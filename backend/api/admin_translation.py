"""Explicit preview/edit/commit; preview drafts expire in Redis, never public Mongo content."""
import asyncio
import json
import secrets
from datetime import datetime, timezone

import httpx
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from pymongo.errors import PyMongoError

from backend.database.mongodb import get_database
from backend.database.redis_client import get_redis_client
from backend.services.admin_auth import require_permission
from backend.services.admin_translation import (
    GoogleTranslator, LANGUAGES, TranslationError, content_hash, revision,
)

router = APIRouter(prefix='/api/admin', tags=['admin-translation'])
PREVIEW_TTL = 1800


class ContentText(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    description: str = Field(min_length=1, max_length=10000)

    @field_validator('title', 'description')
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError('Content must not be blank')
        return value


class SourceText(ContentText):
    source_language: str

    @field_validator('source_language')
    @classmethod
    def supported(cls, value):
        if value not in LANGUAGES:
            raise ValueError('Unsupported source language')
        return value


class PreviewInput(SourceText):
    targets: list[str] = Field(min_length=1, max_length=5)


class TranslationItem(ContentText):
    language_code: str
    replace_existing: bool = False


class CommitInput(BaseModel):
    preview_id: str = Field(pattern=r'^[A-Za-z0-9_-]{32}$')
    items: list[TranslationItem] = Field(min_length=1, max_length=5)


def poi_oid(value):
    if not ObjectId.is_valid(value):
        raise HTTPException(400, 'Invalid POI ID')
    return ObjectId(value)


async def saved_source(db, oid, data, session=None):
    if not await db['poi'].find_one({'_id': oid}, session=session):
        raise HTTPException(404, 'POI not found')
    source = await db['poi_localizations'].find_one(
        {'poi_id': oid, 'language_code': data.source_language}, session=session)
    if not source or source.get('title') != data.title or source.get('description') != data.description:
        raise HTTPException(409, 'Save the current source content first, then request a new translation preview.')
    return source


@router.get('/translation-settings')
async def translation_settings(_=Depends(require_permission('content:write'))):
    translator = GoogleTranslator()
    return {'configured': bool(translator.key), 'provider': translator.provider,
            'languages': list(LANGUAGES), 'preview_ttl_seconds': PREVIEW_TTL}


@router.post('/pois/{poi_id}/translations/preview')
async def preview(poi_id: str, data: PreviewInput,
                  user=Depends(require_permission('content:write')),
                  db=Depends(get_database), redis=Depends(get_redis_client)):
    oid = poi_oid(poi_id)
    if len(set(data.targets)) != len(data.targets) or any(
        target not in LANGUAGES or target == data.source_language for target in data.targets
    ):
        raise HTTPException(422, 'Choose unique target languages different from the source')
    await saved_source(db, oid, data)
    translator = GoogleTranslator()
    if not translator.key:
        raise HTTPException(503, 'Automatic translation is not configured. Set GOOGLE_TRANSLATE_API_KEY on the backend; manual editing remains available.')
    # Shared Redis limit survives backend restarts; one batch per admin per 30 seconds.
    if not await redis.set(f'admin-translation-limit:{user["_id"]}', '1', nx=True, ex=30):
        raise HTTPException(429, 'Wait 30 seconds between translation requests.')
    baselines = {}
    for language in data.targets:
        doc = await db['poi_localizations'].find_one({'poi_id': oid, 'language_code': language})
        baselines[language] = {'revision': revision(doc), 'existing': bool(doc),
                               'existing_title': doc.get('title', '') if doc else '',
                               'existing_description': doc.get('description', '') if doc else ''}
    async with httpx.AsyncClient(timeout=35, follow_redirects=False, trust_env=False) as client:
        async def translate(language):
            try:
                return {'language_code': language, **baselines[language],
                        **await translator.translate(client, data.source_language, language, data.title, data.description)}
            except TranslationError as error:
                return {'language_code': language, 'error': str(error)}
        results = await asyncio.gather(*(translate(language) for language in data.targets))
    token = secrets.token_urlsafe(24)
    document = {'user_id': str(user['_id']), 'poi_id': poi_id, 'source': data.model_dump(exclude={'targets'}),
                'provider': translator.provider, 'results': {row['language_code']: row for row in results if 'error' not in row}}
    await redis.setex(f'admin-translation-preview:{token}', PREVIEW_TTL, json.dumps(document))
    return {'preview_id': token, 'expires_in': PREVIEW_TTL, 'provider': translator.provider, 'results': results}


@router.post('/pois/{poi_id}/translations/commit')
async def commit(poi_id: str, data: CommitInput,
                 user=Depends(require_permission('content:write')),
                 db=Depends(get_database), redis=Depends(get_redis_client)):
    oid = poi_oid(poi_id)
    raw = await redis.get(f'admin-translation-preview:{data.preview_id}')
    if not raw:
        raise HTTPException(409, 'Translation preview expired. Request a new preview.')
    draft = json.loads(raw)
    if draft['user_id'] != str(user['_id']) or draft['poi_id'] != poi_id:
        raise HTTPException(403, 'This preview belongs to another administrator or POI')
    languages = [item.language_code for item in data.items]
    if len(set(languages)) != len(languages) or any(language not in draft['results'] for language in languages):
        raise HTTPException(422, 'Only successful languages in this preview can be saved once per request')
    now = datetime.now(timezone.utc)
    source_data = SourceText(**draft['source'])
    source_digest = content_hash(source_data.title, source_data.description)
    try:
        # Prevent a manual upsert racing a transaction that saw a missing target.
        indexes = await (await db['poi_localizations'].list_indexes()).to_list(length=None)
        if not any(list(index['key'].items()) == [('poi_id', 1), ('language_code', 1)]
                   and index.get('unique') and not index.get('partialFilterExpression')
                   and not index.get('sparse') for index in indexes):
            await db['poi_localizations'].create_index(
                [('poi_id', 1), ('language_code', 1)], unique=True,
                name='uq_poi_localizations_poi_language')
        # Existing deployment uses rs0. All selected targets commit together, or none do.
        async with db.client.start_session() as session:
            async with await session.start_transaction():
                source = await saved_source(db, oid, source_data, session=session)
                # Acquire a source write conflict guard against concurrent source edits.
                await db['poi_localizations'].update_one({'_id': source['_id']},
                    {'$set': {'translation_guard': secrets.token_hex(8)}}, session=session)
                for item in data.items:
                    baseline = draft['results'][item.language_code]
                    previous = await db['poi_localizations'].find_one(
                        {'poi_id': oid, 'language_code': item.language_code}, session=session)
                    if revision(previous) != baseline['revision']:
                        raise HTTPException(409, f'{item.language_code}: content changed since preview; request a new preview.')
                    if previous and not item.replace_existing:
                        raise HTTPException(409, f'{item.language_code}: confirm replacement of existing content.')
                    values = {'title': item.title, 'description': item.description, 'updated_at': now,
                              'translation': {'source_language': source_data.source_language,
                                              'source_hash': source_digest, 'provider': draft['provider'],
                                              'translated_at': now, 'review_status': 'reviewed_by_admin'}}
                    if not previous or previous.get('title') != item.title or previous.get('description') != item.description:
                        values.update({'audio_url': None, 'tts_status': 'draft', 'tts_task_id': None,
                                       'audio_status': 'STALE_REQUIRES_REGENERATION'})
                    await db['poi_localizations'].update_one(
                        {'poi_id': oid, 'language_code': item.language_code},
                        {'$set': values, '$setOnInsert': {'poi_id': oid, 'language_code': item.language_code}},
                        upsert=True, session=session)
                    await db['poi_localizations'].update_many(
                        {'poi_id': oid, 'translation.source_language': item.language_code,
                         'translation.source_hash': {'$ne': content_hash(item.title, item.description)}},
                        {'$set': {'translation.review_status': 'needs_review'}}, session=session)
    except PyMongoError as error:
        # Never retry a transaction automatically: a commit network error can have an unknown result.
        raise HTTPException(409, 'Save could not be confirmed. Reload the POI list and request a new preview before retrying. MongoDB rs0 and unique (poi_id, language_code) records are required; do not delete existing data to bypass this error.') from error
    # Keep the preview until TTL; replay is rejected by revisions, even if this response is lost.
    return {'saved': languages, 'audio_generation_required': True}
