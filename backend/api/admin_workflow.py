import asyncio
import hashlib
import re
from datetime import datetime, timezone
from io import BytesIO

from bson import ObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import Response
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, Field, field_validator

from backend.api.audio import get_audio_storage_provider
from backend.database.mongodb import get_database
from backend.database.redis_client import get_redis_client
from backend.services.admin_auth import require_permission
from backend.services.admin_narration import AdminNarration, VOICES

router = APIRouter(tags=['admin-workflow'])


def oid(value):
    if not ObjectId.is_valid(value):
        raise HTTPException(400, 'Invalid ObjectId')
    return ObjectId(value)


class GeofenceInput(BaseModel):
    radius: float = Field(default=35, ge=5, le=500)
    is_active: bool = False


class NarrationInput(BaseModel):
    voice: str | None = None


class PackageInput(BaseModel):
    language_code: str
    name: str = Field(min_length=1, max_length=180)

    @field_validator('name')
    @classmethod
    def nonempty_name(cls, value):
        if not value.strip():
            raise ValueError('Package name must not be blank')
        return value.strip()


def validate_image(content):
    try:
        with Image.open(BytesIO(content), formats=['JPEG', 'PNG', 'WEBP']) as image:
            if image.width * image.height > 16_000_000:
                raise HTTPException(413, 'Image must not exceed 16 megapixels')
            fmt = image.format
            image.verify()
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError, Image.DecompressionBombError):
        raise HTTPException(422, 'Upload a valid JPEG, PNG or WebP image')
    return {'JPEG': ('jpg', 'image/jpeg'), 'PNG': ('png', 'image/png'), 'WEBP': ('webp', 'image/webp')}[fmt]


@router.post('/api/admin/pois/{poi_id}/image')
async def upload_image(poi_id: str, request: Request, _=Depends(require_permission('poi:write')), db=Depends(get_database), storage=Depends(get_audio_storage_provider)):
    poi = oid(poi_id)
    if not await db['poi'].find_one({'_id': poi}):
        raise HTTPException(404, 'POI not found')
    chunks, size = [], 0
    async for chunk in request.stream():
        size += len(chunk)
        if size > 5 * 1024 * 1024:
            raise HTTPException(413, 'Image must not exceed 5 MB')
        chunks.append(chunk)
    content = b''.join(chunks)
    extension, media_type = await asyncio.to_thread(validate_image, content)
    checksum = hashlib.sha256(content).hexdigest()
    filename = f'{checksum}.{extension}'
    key = f'media/poi/{poi}/{filename}'
    await storage.put(key, content, media_type, checksum)
    url = f'/api/media/pois/{poi}/{filename}'
    await db['poi'].update_one({'_id': poi}, {'$set': {'image_url': url, 'updated_at': datetime.now(timezone.utc)}})
    return {'image_url': url}


@router.get('/api/media/pois/{poi_id}/{filename}')
async def read_image(poi_id: str, filename: str, storage=Depends(get_audio_storage_provider)):
    poi = oid(poi_id)
    if not re.fullmatch(r'[a-f0-9]{64}\.(jpg|png|webp)', filename):
        raise HTTPException(404, 'Image not found')
    obj = await storage.read(f'media/poi/{poi}/{filename}')
    if obj is None:
        raise HTTPException(404, 'Image not found')
    content, _ = obj
    content_type = {'jpg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}[filename.rsplit('.', 1)[1]]
    return Response(content, media_type=content_type, headers={'Cache-Control': 'public, max-age=31536000, immutable', 'X-Content-Type-Options': 'nosniff'})


@router.put('/api/admin/pois/{poi_id}/geofence')
async def save_geofence(poi_id: str, data: GeofenceInput, _=Depends(require_permission('poi:write')), db=Depends(get_database)):
    poi = await db['poi'].find_one({'_id': oid(poi_id)})
    if not poi:
        raise HTTPException(404, 'POI not found')
    if not isinstance(poi.get('latitude'), (float, int)) or not isinstance(poi.get('longitude'), (float, int)):
        raise HTTPException(409, 'Save POI coordinates first')
    now = datetime.now(timezone.utc)
    await db['geofence_zones'].update_one({'poi_id': poi['_id'], 'zone_type': 'circle'}, {'$set': {
        **data.model_dump(), 'geometry': {'type': 'Point', 'coordinates': [poi['longitude'], poi['latitude']]}, 'updated_at': now},
        '$setOnInsert': {'poi_id': poi['_id'], 'zone_type': 'circle', 'created_at': now}}, upsert=True)
    await db['poi'].update_one({'_id': poi['_id']}, {'$set': {'geofence_enabled': data.is_active}})
    return {'saved': True, **data.model_dump()}


@router.get('/api/admin/audio-voices')
async def list_voices(_=Depends(require_permission('audio:write'))):
    return VOICES


@router.post('/api/admin/pois/{poi_id}/localizations/{language}/generate-audio', status_code=202)
async def generate_narration(poi_id: str, language: str, data: NarrationInput, background_tasks: BackgroundTasks,
                             _=Depends(require_permission('audio:write')), db=Depends(get_database),
                             storage=Depends(get_audio_storage_provider), redis=Depends(get_redis_client)):
    service = AdminNarration(db, storage, redis)
    task = await service.enqueue(oid(poi_id), language, data.voice)
    background_tasks.add_task(service.generate, task)
    return {'id': str(task['_id']), 'status': task['status']}


@router.get('/api/admin/audio-jobs/{task_id}')
async def narration_status(task_id: str, _=Depends(require_permission('audio:write')), db=Depends(get_database), storage=Depends(get_audio_storage_provider), redis=Depends(get_redis_client)):
    return await AdminNarration(db, storage, redis).status(oid(task_id))


@router.post('/api/admin/audio-packages', status_code=201)
async def publish_package(data: PackageInput, _=Depends(require_permission('audio:write')), db=Depends(get_database), storage=Depends(get_audio_storage_provider)):
    if data.language_code not in VOICES:
        raise HTTPException(422, 'Unsupported language')
    pois = await db['poi'].find({'is_active': True}).to_list(length=None)
    snapshots = []
    package_id, now = ObjectId(), datetime.now(timezone.utc)
    for poi in pois:
        loc = await db['poi_localizations'].find_one({'poi_id': poi['_id'], 'language_code': data.language_code})
        if not loc or not loc.get('audio_url'):
            continue
        asset = await db['audio_assets'].find_one({'poi_id': poi['_id'], 'language_code': data.language_code, 'file_url': loc['audio_url']})
        if not asset:
            raise HTTPException(409, 'A recording has no asset metadata. Regenerate it before publishing.')
        if asset:
            info = await storage.inspect(asset['file_url'])
            if not info or not info.size or info.checksum != asset['checksum']:
                raise HTTPException(409, 'A recording is missing or invalid. Regenerate it before publishing.')
            snapshots.append({**asset, '_id': ObjectId(), 'package_id': package_id, 'is_snapshot': True, 'created_at': now, 'size_bytes': info.size})
    if not snapshots:
        raise HTTPException(409, 'No active POIs have ready audio in this language')
    # Publish the package record last; incomplete snapshots cannot be listed/downloaded.
    try:
        await db['audio_assets'].insert_many(snapshots)
        await db['audio_packages'].insert_one({'_id': package_id, 'name': data.name.strip(), 'language_code': data.language_code,
            'description': 'Published recording snapshot', 'file_url': f'packages/{package_id}.manifest.json',
            'file_size': sum(row['size_bytes'] for row in snapshots), 'is_offline': True, 'is_snapshot': True, 'created_at': now})
    except Exception:
        await db['audio_assets'].delete_many({'package_id': package_id, 'is_snapshot': True})
        raise
    return {'id': str(package_id), 'name': data.name, 'asset_count': len(snapshots)}
