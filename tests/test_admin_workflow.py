import copy
import hashlib
import unittest
from datetime import datetime, timedelta, timezone
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from bson import ObjectId
from fastapi import HTTPException
from fastapi.testclient import TestClient
from PIL import Image

from backend.api.admin_workflow import GeofenceInput, PackageInput, publish_package, save_geofence, validate_image
from backend.api.admin import PoiCreateInput, create_poi, LocalizationInput, save_localization
from backend.api.audio import get_audio_storage_provider
from backend.database.mongodb import get_database
from backend.main import app
from backend.services.admin_auth import require_admin
from backend.services.admin_narration import AdminNarration
from backend.services.admin_narration import synthesize
from backend.services.audio_storage import StorageObjectMetadata
from backend.services.audio import AudioService


class Cursor:
    def __init__(self, rows): self.rows = rows
    def sort(self, *args): return self
    async def to_list(self, length=None): return copy.deepcopy(self.rows[:length])


class Collection:
    def __init__(self): self.rows = []
    def matches(self, row, query):
        return all(row.get(k) in v['$in'] if isinstance(v, dict) and '$in' in v else row.get(k) == v for k, v in query.items())
    async def find_one(self, query, **kwargs):
        return next((copy.deepcopy(r) for r in self.rows if self.matches(r, query)), None)
    def find(self, query): return Cursor([r for r in self.rows if self.matches(r, query)])
    async def insert_one(self, row):
        row = copy.deepcopy(row); row.setdefault('_id', ObjectId()); self.rows.append(row)
        return SimpleNamespace(inserted_id=row['_id'])
    async def insert_many(self, rows):
        for row in rows: await self.insert_one(row)
    async def update_one(self, query, update, upsert=False):
        for row in self.rows:
            if self.matches(row, query):
                row.update(copy.deepcopy(update.get('$set', {})))
                return SimpleNamespace(matched_count=1)
        if upsert:
            await self.insert_one({**query, **update.get('$setOnInsert', {}), **update.get('$set', {})})
        return SimpleNamespace(matched_count=0)
    async def delete_many(self, query): self.rows = [r for r in self.rows if not self.matches(r, query)]
    async def delete_one(self, query):
        for row in self.rows:
            if self.matches(row, query):
                self.rows.remove(row)
                return


class Database:
    def __init__(self): self.collections = {}
    def __getitem__(self, key): return self.collections.setdefault(key, Collection())


class Redis:
    def __init__(self): self.values = {}
    async def set(self, key, value, nx=False, ex=None):
        if nx and key in self.values: return False
        self.values[key] = value; return True
    async def eval(self, script, count, key, value):
        if self.values.get(key) == value: self.values.pop(key)


class Storage:
    def __init__(self): self.objects = {}
    async def put(self, key, content, media_type, checksum): self.objects[key] = (content, media_type, checksum)
    async def read(self, key):
        obj = self.objects.get(key)
        return (obj[0], obj[1]) if obj else None
    async def inspect(self, key):
        obj = self.objects.get(key)
        return StorageObjectMetadata(len(obj[0]), obj[2]) if obj else None


class NarrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_transient_provider_failure_retries_once(self):
        from edge_tts.exceptions import NoAudioReceived
        with patch('backend.services.admin_narration._synthesize_once', AsyncMock(side_effect=[NoAudioReceived('No audio'), (b'mp3', 1)])) as generate:
            with patch('backend.services.admin_narration.asyncio.sleep', AsyncMock()):
                self.assertEqual(await synthesize('Text', 'voice'), (b'mp3', 1))
        self.assertEqual(generate.await_count, 2)

    async def asyncSetUp(self):
        self.db, self.storage, self.redis = Database(), Storage(), Redis()
        self.poi = ObjectId()
        await self.db['poi'].insert_one({'_id': self.poi, 'is_active': True, 'latitude': 10.788, 'longitude': 106.706})
        await self.db['poi_localizations'].insert_one({'poi_id': self.poi, 'language_code': 'vi', 'title': 'Test', 'description': 'Saved narration', 'audio_url': None})
        self.service = AdminNarration(self.db, self.storage, self.redis)

    async def test_success_registers_asset_and_releases_lock(self):
        task = await self.service.enqueue(self.poi, 'vi')
        with patch('backend.services.admin_narration.synthesize', AsyncMock(return_value=(b'audio', 1.2))):
            await self.service.generate(task)
        loc = await self.db['poi_localizations'].find_one({'poi_id': self.poi})
        asset = await self.db['audio_assets'].find_one({'file_url': loc['audio_url']})
        self.assertEqual(asset['checksum'], hashlib.sha256(b'audio').hexdigest())
        self.assertIsInstance(loc['tts_task_id'], ObjectId)
        self.assertEqual((await self.service.status(task['_id']))['status'], 'Completed')
        self.assertFalse(self.redis.values)

    async def test_duplicate_job_is_rejected(self):
        await self.service.enqueue(self.poi, 'vi')
        with self.assertRaises(HTTPException) as error: await self.service.enqueue(self.poi, 'vi')
        self.assertEqual(error.exception.status_code, 409)

    async def test_unsupported_voice_and_missing_translation_are_rejected(self):
        with self.assertRaises(HTTPException): await self.service.enqueue(self.poi, 'vi', 'en-US-AvaNeural')
        with self.assertRaises(HTTPException): await self.service.enqueue(self.poi, 'fr')

    async def test_changed_content_cannot_be_overwritten_by_late_audio(self):
        task = await self.service.enqueue(self.poi, 'vi')
        await self.db['poi_localizations'].update_one({'poi_id': self.poi}, {'$set': {'description': 'New text', 'tts_task_id': None}})
        with patch('backend.services.admin_narration.synthesize', AsyncMock(return_value=(b'old narration', 1))):
            await self.service.generate(task)
        loc = await self.db['poi_localizations'].find_one({'poi_id': self.poi})
        self.assertIsNone(loc['audio_url'])
        self.assertEqual((await self.service.status(task['_id']))['status'], 'Failed')

    async def test_provider_failure_allows_retry(self):
        task = await self.service.enqueue(self.poi, 'vi')
        with patch('backend.services.admin_narration.synthesize', AsyncMock(side_effect=TimeoutError())):
            await self.service.generate(task)
        self.assertEqual((await self.service.status(task['_id']))['status'], 'Failed')
        self.assertNotEqual((await self.service.enqueue(self.poi, 'vi'))['_id'], task['_id'])

    async def test_new_generation_preserves_previously_published_package(self):
        async def generate(content):
            task = await self.service.enqueue(self.poi, 'vi')
            with patch('backend.services.admin_narration.synthesize', AsyncMock(return_value=(content, 1))): await self.service.generate(task)
        await generate(b'first')
        package = await publish_package(PackageInput(language_code='vi', name='First'), db=self.db, storage=self.storage)
        snapshot = await self.db['audio_assets'].find_one({'package_id': ObjectId(package['id'])})
        await generate(b'second')
        unchanged = await self.db['audio_assets'].find_one({'_id': snapshot['_id']})
        self.assertEqual(unchanged, snapshot)
        self.assertEqual((await self.storage.read(snapshot['file_url']))[0], b'first')
        loc = await self.db['poi_localizations'].find_one({'poi_id': self.poi})
        self.assertNotEqual(loc['audio_url'], snapshot['file_url'])

    async def test_snapshot_package_and_asset_membership_cannot_be_reassigned(self):
        service = AudioService(self.db, self.storage)
        package_id, asset_id, legacy_id = ObjectId(), ObjectId(), ObjectId()
        await self.db['audio_packages'].insert_one({'_id': package_id, 'is_snapshot': True})
        await self.db['audio_packages'].insert_one({'_id': legacy_id, 'language_code': 'vi'})
        await self.db['audio_assets'].insert_one({'_id': asset_id, 'is_snapshot': True, 'language_code': 'vi'})
        for target in (package_id, legacy_id):
            with self.assertRaises(HTTPException) as error: await service.assign_asset(str(target), str(asset_id))
            self.assertEqual(error.exception.status_code, 409)

    async def test_package_rejects_missing_storage_audio(self):
        await self.db['poi_localizations'].update_one({'poi_id': self.poi}, {'$set': {'audio_url': 'missing.mp3'}})
        await self.db['audio_assets'].insert_one({'poi_id': self.poi, 'language_code': 'vi', 'file_url': 'missing.mp3', 'checksum': 'abc'})
        with self.assertRaises(HTTPException): await publish_package(PackageInput(language_code='vi', name='Missing'), db=self.db, storage=self.storage)
        self.assertFalse(self.db['audio_packages'].rows)

    async def test_geofence_uses_saved_coordinates(self):
        await save_geofence(str(self.poi), GeofenceInput(radius=42, is_active=True), db=self.db)
        zone = await self.db['geofence_zones'].find_one({'poi_id': self.poi})
        self.assertEqual(zone['geometry']['coordinates'], [106.706, 10.788])
        self.assertEqual(zone['radius'], 42)

    async def test_interrupted_job_becomes_retryable(self):
        task = await self.service.enqueue(self.poi, 'vi')
        await self.db['audio_tasks'].update_one({'_id': task['_id']}, {'$set': {'updated_at': datetime.now(timezone.utc) - timedelta(minutes=6)}})
        self.assertEqual((await self.service.status(task['_id']))['status'], 'Failed')
        self.assertEqual((await self.db['poi_localizations'].find_one({'poi_id': self.poi}))['tts_status'], 'Failed')

    async def test_save_unchanged_text_keeps_ready_audio_but_changed_text_invalidates_it(self):
        await self.db['poi_localizations'].update_one({'poi_id': self.poi}, {'$set': {'audio_url': 'ready.mp3', 'tts_status': 'Completed'}})
        await save_localization(str(self.poi), 'vi', LocalizationInput(title='Test', description='Saved narration'), db=self.db)
        loc = await self.db['poi_localizations'].find_one({'poi_id': self.poi})
        self.assertEqual((loc['audio_url'], loc['tts_status']), ('ready.mp3', 'Completed'))
        await save_localization(str(self.poi), 'vi', LocalizationInput(title='Test', description='New narration'), db=self.db)
        loc = await self.db['poi_localizations'].find_one({'poi_id': self.poi})
        self.assertIsNone(loc['audio_url'])
        self.assertIsNone(loc['tts_task_id'])

    async def test_create_with_localization_is_hidden_by_default_and_checks_both_permissions(self):
        data = PoiCreateInput(name='New POI', category='animal_exhibit', description='Description', latitude=10.788, longitude=106.706,
            initial_localization={'language_code': 'vi', 'title': 'New title', 'description': 'Description'})
        with self.assertRaises(HTTPException) as error:
            await create_poi(data, user={'permissions': ['poi:write']}, db=self.db)
        self.assertEqual(error.exception.status_code, 403)
        created = await create_poi(data, user={'permissions': ['poi:write', 'content:write']}, db=self.db)
        poi = await self.db['poi'].find_one({'_id': ObjectId(created['id'])})
        self.assertFalse(poi['is_active'])
        self.assertEqual((await self.db['poi_localizations'].find_one({'poi_id': poi['_id']}))['title'], 'New title')

    async def test_failed_initial_localization_removes_partial_new_poi(self):
        before = len(self.db['poi'].rows)
        data = PoiCreateInput(name='New', category='animal_exhibit', description='Description', latitude=10.788, longitude=106.706,
            initial_localization={'language_code': 'vi', 'title': 'New', 'description': 'Description'})
        with patch.object(self.db['poi_localizations'], 'insert_one', AsyncMock(side_effect=RuntimeError('Unavailable'))):
            with self.assertRaises(RuntimeError): await create_poi(data, user={'permissions': ['content:write']}, db=self.db)
        self.assertEqual(len(self.db['poi'].rows), before)


class ImageAndAuthorizationTests(unittest.TestCase):
    def tearDown(self): app.dependency_overrides.clear()

    def test_real_image_validation_rejects_svg_and_excess_pixels(self):
        with self.assertRaises(HTTPException): validate_image(b'<svg onload="bad"/>')
        out = BytesIO(); Image.new('RGB', (20, 20), 'green').save(out, format='PNG')
        self.assertEqual(validate_image(out.getvalue()), ('png', 'image/png'))
        out = BytesIO(); Image.new('RGB', (4001, 4001)).save(out, format='PNG')
        with self.assertRaises(HTTPException) as error: validate_image(out.getvalue())
        self.assertEqual(error.exception.status_code, 413)

    def test_workflow_writes_require_permissions(self):
        with TestClient(app, raise_server_exceptions=False) as client:
            self.assertEqual(client.post(f'/api/admin/pois/{ObjectId()}/image', content=b'bad').status_code, 401)
            self.assertEqual(client.post('/api/admin/audio-packages', json={'language_code':'vi','name':'Test'}).status_code, 401)
        app.dependency_overrides[require_admin] = lambda: {'permissions': []}
        with TestClient(app, raise_server_exceptions=False) as client:
            self.assertEqual(client.get('/api/admin/audio-voices').status_code, 403)

    def test_image_upload_stores_verified_bytes_and_public_endpoint_serves_same_image(self):
        db, storage = Database(), Storage()
        poi = ObjectId(); db['poi'].rows.append({'_id':poi})
        app.dependency_overrides[get_database] = lambda: db
        app.dependency_overrides[get_audio_storage_provider] = lambda: storage
        app.dependency_overrides[require_admin] = lambda: {'permissions':['poi:write']}
        out = BytesIO(); Image.new('RGB', (20,20), 'green').save(out, format='PNG')
        with TestClient(app) as client:
            result = client.post(f'/api/admin/pois/{poi}/image', content=out.getvalue(), headers={'Content-Type':'image/png'})
            self.assertEqual(result.status_code, 200)
            image = client.get(result.json()['image_url'])
            self.assertEqual(image.content, out.getvalue())
            self.assertEqual(image.headers['x-content-type-options'], 'nosniff')
            self.assertEqual(client.post(f'/api/admin/pois/{poi}/image', content=b'x'*(5*1024*1024+1)).status_code, 413)
