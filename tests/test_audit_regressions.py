import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from bson import ObjectId
from fastapi.testclient import TestClient

from backend.api.admin import LocalizationInput, PoiInput, analytics_summary, save_localization, update_poi
from backend.api.visitor import EventRequest, record_event
from backend.main import app
from backend.services.admin_auth import require_admin


class AuthorizationRegressionTests(unittest.TestCase):
    def tearDown(self):
        app.dependency_overrides.clear()

    def test_anonymous_admin_and_audio_writes_are_denied(self):
        with TestClient(app, raise_server_exceptions=False) as client:
            for url in ['/api/admin/pois', '/api/admin/analytics/summary', '/audio/tasks/' + str(ObjectId())]:
                self.assertEqual(client.get(url).status_code, 401)
            self.assertEqual(client.post('/audio/packages', json={}).status_code, 401)

    def test_authenticated_user_without_permission_is_denied(self):
        app.dependency_overrides[require_admin] = lambda: {'permissions': []}
        with TestClient(app, raise_server_exceptions=False) as client:
            self.assertEqual(client.get('/api/admin/analytics/summary').status_code, 403)
            self.assertEqual(client.get('/api/admin/pois').status_code, 403)


class DataRegressionTests(unittest.IsolatedAsyncioTestCase):
    def make_db(self):
        collections = {}
        db = MagicMock()
        db.__getitem__.side_effect = lambda name: collections.setdefault(name, AsyncMock())
        return db

    async def test_editing_translation_invalidates_old_narration(self):
        db = self.make_db()
        db['poi'].find_one.return_value = {'_id': ObjectId()}
        db['poi_localizations'].find_one.return_value = {'title': 'Before', 'description': 'Old text', 'audio_url': 'old.mp3'}
        await save_localization(str(ObjectId()), 'vi', LocalizationInput(title='After', description='New text'), db=db)
        values = db['poi_localizations'].update_one.call_args.args[1]['$set']
        self.assertIsNone(values['audio_url'])
        self.assertEqual(values['tts_status'], 'draft')

    async def test_unchanged_translation_keeps_audio(self):
        db = self.make_db()
        db['poi'].find_one.return_value = {'_id': ObjectId()}
        db['poi_localizations'].find_one.return_value = {'title': 'Same', 'description': 'Same text', 'audio_url': 'same.mp3'}
        await save_localization(str(ObjectId()), 'vi', LocalizationInput(title='Same', description='Same text'), db=db)
        self.assertNotIn('audio_url', db['poi_localizations'].update_one.call_args.args[1]['$set'])

    async def test_moving_poi_moves_its_circle_geofences(self):
        db = self.make_db()
        db['poi'].update_one.return_value = SimpleNamespace(matched_count=1)
        oid = ObjectId()
        await update_poi(str(oid), PoiInput(name='Test', category='animal', description='Test', latitude=10.7, longitude=106.7), db=db)
        query, update = db['geofence_zones'].update_many.call_args.args
        self.assertEqual(query, {'poi_id': oid, 'zone_type': 'circle'})
        self.assertEqual(update['$set']['geometry']['coordinates'], [106.7, 10.7])

    async def test_visit_charts_count_session_starts(self):
        db = self.make_db()
        events = db['analytics_events']
        events.count_documents.return_value = 0
        cursor = AsyncMock()
        cursor.to_list.return_value = []
        events.aggregate.return_value = cursor
        await analytics_summary(db=db)
        pipelines = [call.args[0] for call in events.aggregate.call_args_list]
        charts = [p for p in pipelines if any('$group' in stage and ('$dateToString' in str(stage) or '$hour' in str(stage)) for stage in p)]
        self.assertEqual(len(charts), 2)
        self.assertTrue(all(p[0]['$match']['event_type'] == 'session_start' for p in charts))

    async def test_visitor_ids_remain_objectids_and_session_start_is_upserted(self):
        db = self.make_db()
        redis = AsyncMock()
        redis.incr.return_value = 1
        visitor = ObjectId()
        payload = EventRequest(visitor_id=str(visitor), device_id=str(ObjectId()), session_id=str(ObjectId()), event_type='session_start', language_code='fr')
        with patch('backend.api.visitor.get_redis_client', return_value=redis):
            await record_event(payload, database=db)
        session = db['analytics_sessions'].update_one.call_args.args[1]['$setOnInsert']
        self.assertEqual(session['user_id'], visitor)
        db['analytics_events'].insert_one.assert_not_called()
        self.assertTrue(db['analytics_events'].update_one.call_args.kwargs['upsert'])
