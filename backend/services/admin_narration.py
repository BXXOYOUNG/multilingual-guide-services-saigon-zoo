"""Admin-triggered TTS, using the existing audio collections and S3 adapter."""
import asyncio
import hashlib
import logging
import os
from datetime import datetime, timedelta, timezone
from io import BytesIO

from bson import ObjectId
from fastapi import HTTPException

logger = logging.getLogger(__name__)
VOICES = {
    'vi': ['vi-VN-HoaiMyNeural', 'vi-VN-NamMinhNeural'],
    'en': ['en-US-AvaNeural', 'en-US-AndrewNeural'],
    'fr': ['fr-FR-DeniseNeural', 'fr-FR-HenriNeural'],
    'zh-Hans': ['zh-CN-XiaoxiaoNeural', 'zh-CN-YunxiNeural'],
    'ja': ['ja-JP-NanamiNeural', 'ja-JP-KeitaNeural'],
    'ko': ['ko-KR-SunHiNeural', 'ko-KR-InJoonNeural'],
}


async def synthesize(text, voice):
    from aiohttp import ClientError
    from edge_tts.exceptions import NoAudioReceived
    for attempt in range(2):
        try:
            return await _synthesize_once(text, voice)
        except (ClientError, NoAudioReceived, TimeoutError):
            if attempt:
                raise
            await asyncio.sleep(1)


async def _synthesize_once(text, voice):
    import edge_tts
    from mutagen.mp3 import MP3
    chunks, size = [], 0
    async for item in edge_tts.Communicate(text, voice, connect_timeout=10, receive_timeout=30).stream():
        if item['type'] == 'audio':
            size += len(item['data'])
            if size > 20 * 1024 * 1024:
                raise ValueError('Generated audio exceeds limit')
            chunks.append(item['data'])
    audio = b''.join(chunks)
    if len(audio) < 1024:
        raise ValueError('Empty or invalid audio')
    duration = MP3(BytesIO(audio)).info.length
    return audio, duration


class AdminNarration:
    def __init__(self, db, storage, redis):
        self.db, self.storage, self.redis = db, storage, redis

    async def enqueue(self, poi_id, language, voice=None):
        if language not in VOICES or (voice and voice not in VOICES[language]):
            raise HTTPException(422, 'Unsupported language or voice')
        if os.getenv('TTS_PROVIDER', 'edge-tts') != 'edge-tts':
            raise HTTPException(503, 'TTS provider is disabled')
        poi = await self.db['poi'].find_one({'_id': poi_id})
        loc = await self.db['poi_localizations'].find_one({'poi_id': poi_id, 'language_code': language})
        if not poi or not loc or not loc.get('description', '').strip():
            raise HTTPException(404, 'Save a POI localization before generating audio')
        task_id, now = ObjectId(), datetime.now(timezone.utc)
        key = f'admin-tts:{poi_id}:{language}'
        if not await self.redis.set(key, str(task_id), nx=True, ex=300):
            raise HTTPException(409, 'An audio generation is already running for this language. Retry after it completes.')
        task = {'_id': task_id, 'poi_id': poi_id, 'language_code': language, 'type': 'TTS', 'status': 'Pending', 'file_url': None,
                'voice': voice or VOICES[language][0], 'source_title': loc['title'], 'source_text': loc['description'],
                'created_at': now, 'updated_at': now, 'error_message': None}
        try:
            await self.db['audio_tasks'].insert_one(task)
            result = await self.db['poi_localizations'].update_one(
                {'_id': loc['_id'], 'title': loc['title'], 'description': loc['description']},
                {'$set': {'tts_status': 'Pending', 'tts_task_id': task_id}})
            if not result.matched_count:
                raise HTTPException(409, 'Content changed. Reload and generate again.')
        except Exception:
            await self._unlock(key, task_id)
            await self.db['audio_tasks'].update_one({'_id': task_id}, {'$set': {'status': 'Failed', 'error_message': 'Unable to queue current content'}})
            raise
        return task

    async def _unlock(self, key, task_id):
        try:
            await self.redis.eval("if redis.call('get',KEYS[1])==ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end", 1, key, str(task_id))
        except Exception:
            # The lease expires automatically; a Redis outage must not erase the job result.
            logger.exception('Unable to release admin TTS lease: %s', task_id)

    async def generate(self, task):
        task_id, poi_id, language = task['_id'], task['poi_id'], task['language_code']
        current = {'poi_id': poi_id, 'language_code': language, 'tts_task_id': task_id,
                   'title': task['source_title'], 'description': task['source_text']}
        try:
            await self.db['audio_tasks'].update_one({'_id': task_id}, {'$set': {'status': 'Processing', 'updated_at': datetime.now(timezone.utc)}})
            await self.db['poi_localizations'].update_one(current, {'$set': {'tts_status': 'Processing'}})
            audio, duration = await asyncio.wait_for(synthesize(task['source_text'], task['voice']), timeout=180)
            checksum = hashlib.sha256(audio).hexdigest()
            # Immutable object keys preserve previously published/downloaded packages.
            key = f'narration/{poi_id}/{language}/{task_id}.mp3'
            await self.storage.put(key, audio, 'audio/mpeg', checksum)
            now = datetime.now(timezone.utc)
            asset = {'_id': ObjectId(), 'poi_id': poi_id, 'language_code': language, 'package_id': None,
                     'file_url': key, 'checksum': checksum, 'duration': duration, 'size_bytes': len(audio),
                     'voice': task['voice'], 'created_at': now, 'source_task_id': task_id}
            await self.db['audio_assets'].insert_one(asset)
            result = await self.db['poi_localizations'].update_one(current, {'$set': {
                'audio_url': key, 'audio_status': 'READY', 'tts_status': 'Completed', 'updated_at': now}})
            if not result.matched_count:
                raise ValueError('Content changed while audio was generating')
            await self.db['audio_tasks'].update_one({'_id': task_id}, {'$set': {
                'status': 'Completed', 'file_url': key, 'updated_at': now, 'error_message': None}})
        except Exception:
            logger.exception('Admin TTS job failed: %s', task_id)
            message = 'Audio generation failed or content changed. Check the connection, reload and retry.'
            await self.db['audio_tasks'].update_one({'_id': task_id}, {'$set': {'status': 'Failed', 'error_message': message, 'updated_at': datetime.now(timezone.utc)}})
            await self.db['poi_localizations'].update_one(current, {'$set': {'tts_status': 'Failed'}})
        finally:
            await self._unlock(f'admin-tts:{poi_id}:{language}', task_id)

    async def status(self, task_id):
        task = await self.db['audio_tasks'].find_one({'_id': task_id})
        if not task:
            raise HTTPException(404, 'Audio task not found')
        updated = task.get('updated_at', task['created_at'])
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=timezone.utc)
        if task['status'] in {'Pending', 'Processing'} and updated < datetime.now(timezone.utc) - timedelta(minutes=5):
            task.update(status='Failed', error_message='Generation was interrupted. Retry this recording.')
            await self.db['audio_tasks'].update_one({'_id': task_id, 'status': {'$in': ['Pending', 'Processing']}}, {'$set': {'status': task['status'], 'error_message': task['error_message']}})
            await self.db['poi_localizations'].update_one({'tts_task_id': task_id}, {'$set': {'tts_status': 'Failed'}})
        return {'id': str(task['_id']), 'status': task['status'], 'error_message': task.get('error_message'), 'voice': task.get('voice')}
