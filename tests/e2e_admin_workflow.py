"""Opt-in live admin workflow audit. Requires the local demo, Docker and Internet.

Run: .venv/Scripts/python.exe tests/e2e_admin_workflow.py
Creates only disposable records, intercepts analytics and removes its own data.
Real Edge TTS is used; no provider responses are mocked.
"""
import json
import os
import secrets
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import boto3
from bson import ObjectId
from playwright.sync_api import sync_playwright, expect
from pymongo import MongoClient
from backend.services.admin_auth import hash_password


def main():
    mongo = MongoClient('mongodb://127.0.0.1:27018/?replicaSet=rs0')
    db = mongo['saigon_zoo_tcv_dataset_dev']
    tag, password = 'workflow-audit-' + secrets.token_hex(5), secrets.token_urlsafe(24)
    role = db.roles.find_one({'name': 'administrator'})
    uid = db.admin_users.insert_one({'username': tag, 'email': tag + '@localhost.invalid',
        'password_hash': hash_password(password), 'role_id': role['_id'], 'is_active': True,
        'created_at': datetime.now(timezone.utc)}).inserted_id
    package_ids, poi_ids, errors, checks = [], [], [], []
    out = ROOT / '.demo-run/admin-workflow-audit'
    out.mkdir(parents=True, exist_ok=True)
    base = 'http://localhost:3000'
    try:
        with sync_playwright() as pw:
            chrome = next((Path(os.environ['LOCALAPPDATA']) / 'ms-playwright').glob('chromium-*/chrome-win64/chrome.exe'))
            browser = pw.chromium.launch(executable_path=str(chrome), headless=True)
            context = browser.new_context(viewport={'width': 1440, 'height': 1000})
            context.add_init_script("localStorage.setItem('saigon_zoo_selected_language','vi')")
            context.route('**/api/analytics/events', lambda route: route.fulfill(status=202, json={'accepted': True}))
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(base + '/admin')
            page.locator('input[autocomplete=username]').fill(tag)
            page.locator('input[autocomplete=current-password]').fill(password)
            page.locator('.admin-login form button').click()
            page.get_by_role('button', name='Thêm POI', exact=True).click()
            dialog = page.locator('dialog[open]')
            dialog.get_by_label('Tên hệ thống', exact=True).fill(tag)
            dialog.get_by_label('Tiêu đề hiển thị', exact=False).fill(tag)
            dialog.get_by_label('Tên khoa học', exact=True).fill('Panthera tigris')
            dialog.locator('textarea').fill('Đây là lời thuyết minh kiểm thử. Xin chào quý khách đến với Thảo Cầm Viên.')
            dialog.locator('input[type=file]').set_input_files(str(ROOT / 'frontend/public/images/animals/bengal-tiger.jpg'))
            dialog.get_by_label('Vĩ độ', exact=True).fill('10.788')
            dialog.get_by_label('Kinh độ', exact=True).fill('106.706')
            dialog.get_by_label('Bán kính vùng tự phát (m)', exact=True).fill('42')
            dialog.get_by_label('Bật vùng kích hoạt audio', exact=True).check()
            dialog.get_by_role('button', name='Lưu và tạo audio', exact=True).click()
            page.wait_for_function("document.querySelector('.admin-narration-panel')", timeout=30000)
            record = db.poi.find_one({'name': tag})
            assert record, 'POI not saved'
            poi_id = str(record['_id']); poi_ids.append(record['_id'])
            assert not record['is_active']
            expect(dialog.locator('audio')).to_be_visible(timeout=210000)
            record = db.poi.find_one({'_id': record['_id']})
            assert record['image_url'].startswith('/api/media/pois/')
            assert context.request.get(base + record['image_url']).ok
            zone = db.geofence_zones.find_one({'poi_id': record['_id']})
            assert zone['radius'] == 42 and zone['is_active']
            page.wait_for_function("document.querySelector('dialog audio')?.readyState >= 1", timeout=30000)
            assert page.locator('dialog audio').evaluate('(a) => a.duration > 0')
            checks.append('UI creates hidden POI, uploads a real image, saves geofence and synthesizes playable Vietnamese MP3')
            print('PASS create/image/geofence/real TTS', flush=True)
            page.screenshot(path=str(out / 'create-and-audio-desktop.png'), full_page=True)
            page.set_viewport_size({'width': 390, 'height': 844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2')
            assert dialog.evaluate('(d) => d.scrollWidth <= d.clientWidth + 2')
            page.screenshot(path=str(out / 'create-and-audio-mobile.png'), full_page=True)
            dialog.get_by_label('Hiển thị trên bản đồ', exact=True).check()
            dialog.get_by_role('button', name='Lưu', exact=True).click()
            expect(dialog.get_by_text('Đã lưu. Có thể nghe thử, chỉnh lại hoặc đóng cửa sổ.', exact=True)).to_be_visible()
            dialog.get_by_role('button', name='Đóng', exact=True).last.click()
            catalog = context.request.get(base + '/api/pois/catalog?language=vi').json()
            assert any(row['id'] == poi_id and row['image_url'] == record['image_url'] for row in catalog)
            assert not any(row['id'] == poi_id for row in context.request.get(base + '/api/pois?language=en').json())
            checks.append('Responsive form and publication to localized public catalog')
            # Use the UI to publish a package; track the response before further assertions.
            with page.expect_response(lambda r: r.url.endswith('/api/admin/audio-packages') and r.request.method == 'POST', timeout=60000) as pending:
                page.get_by_role('button', name='Phát hành gói audio mới', exact=True).click()
            response = pending.value
            assert response.status == 201, response.text()
            pack = response.json(); package_ids.append(ObjectId(pack['id']))
            manifest_url = base + f"/audio/packages/{pack['id']}/manifest"
            original_manifest = context.request.get(manifest_url).json()
            assert any(row['poi_id'] == poi_id for row in original_manifest['assets'])
            assert original_manifest['integrity_status'] == 'verified'
            page.goto(base)
            expect(page.locator(f'a[href="/explore?package={pack["id"]}"]')).to_have_count(1)
            page.goto(base + f"/explore?package={pack['id']}")
            page.wait_for_function('!location.search', timeout=120000)
            page.goto(base + f'/map?poi={poi_id}')
            expect(page.locator('.poi-detail-image')).to_be_visible(timeout=30000)
            page.wait_for_function("document.querySelector('.poi-detail-image')?.naturalWidth > 0")
            context.set_offline(True)
            page.reload()
            expect(page.locator('.poi-detail-image')).to_be_visible(timeout=30000)
            page.wait_for_function("document.querySelector('.poi-detail-image')?.naturalWidth > 0")
            page.goto(base + '/explore')
            audio_row = page.locator('.offline-package-row').filter(has_text=tag)
            # The offline list identifies recordings by POI ID; play the disposable recording.
            if not audio_row.count():
                audio_row = page.locator('.offline-package-row').last
            audio_row.get_by_role('button').first.click()
            page.wait_for_function("Array.from(document.querySelectorAll('audio')).some(a => a.readyState >= 1 && a.duration > 0)", timeout=30000)
            context.set_offline(False)
            checks.append('Published QR appears on home; package download, uploaded image and playable audio survive offline navigation')
            print('PASS snapshot/QR/download/offline', flush=True)
            # Update the narration and generate a new file: published snapshot must remain stable.
            new_text = 'Hổ Bengal là loài mèo lớn với bộ lông màu cam và những vằn đen đặc trưng. Mỗi cá thể có hoa văn vằn riêng, giúp chúng ẩn mình giữa cây cỏ.'
            update = context.request.put(base + f'/api/admin/pois/{poi_id}/localizations/vi', data={'title': tag, 'description': new_text})
            assert update.ok
            assert db.poi_localizations.find_one({'poi_id': record['_id'], 'language_code': 'vi'})['description'] == new_text
            queued = context.request.post(base + f'/api/admin/pois/{poi_id}/localizations/vi/generate-audio', data={})
            assert queued.status == 202
            deadline = time.monotonic() + 210
            while time.monotonic() < deadline:
                status = context.request.get(base + '/api/admin/audio-jobs/' + queued.json()['id']).json()
                if status['status'] in {'Completed', 'Failed'}: break
                page.wait_for_timeout(1000)
            if status['status'] != 'Completed':
                stable = lambda manifest: [(a['id'], a['poi_id'], a['checksum'], a['size_bytes']) for a in manifest['assets']]
                assert stable(context.request.get(manifest_url).json()) == stable(original_manifest)
                (out / 'results.json').write_text(json.dumps({'passed': checks, 'page_errors': errors,
                    'incomplete': 'Real-provider regeneration did not complete', 'job': status,
                    'old_snapshot_preserved': True}, ensure_ascii=False, indent=2), encoding='utf-8')
                context.request.post(base + '/api/admin/auth/logout')
                raise AssertionError(f'Real TTS provider regeneration failed: {status}')
            current = db.poi_localizations.find_one({'poi_id': record['_id'], 'language_code': 'vi'})
            previous = next(row for row in original_manifest['assets'] if row['poi_id'] == poi_id)
            assert current['audio_url'] != db.audio_assets.find_one({'_id': ObjectId(previous['id'])})['file_url']
            stable = lambda manifest: [(a['id'], a['poi_id'], a['checksum'], a['size_bytes']) for a in manifest['assets']]
            assert stable(context.request.get(manifest_url).json()) == stable(original_manifest)
            checks.append('Regenerating changed text leaves the old published manifest unchanged')
            assert not errors, errors
            context.request.post(base + '/api/admin/auth/logout')
            browser.close()
        (out / 'results.json').write_text(json.dumps({'passed': checks, 'page_errors': errors}, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'passed': checks, 'page_errors': errors}, ensure_ascii=True, indent=2))
    finally:
        # Also discover a partially created record if a browser assertion failed early.
        poi_ids = list(set(poi_ids + [r['_id'] for r in db.poi.find({'name': tag}, {'_id': 1})]))
        config = json.loads(subprocess.check_output(['docker', 'inspect', 'saigon-zoo-t10-seaweedfs'], text=True))[0]
        env = dict(item.split('=', 1) for item in config['Config']['Env'] if '=' in item)
        s3 = boto3.client('s3', endpoint_url='http://127.0.0.1:8333', aws_access_key_id=env['AWS_ACCESS_KEY_ID'], aws_secret_access_key=env['AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
        for poi in poi_ids:
            for prefix in (f'narration/{poi}/', f'media/poi/{poi}/'):
                for result in s3.get_paginator('list_objects_v2').paginate(Bucket=env['S3_BUCKET'], Prefix=prefix):
                    for obj in result.get('Contents', []): s3.delete_object(Bucket=env['S3_BUCKET'], Key=obj['Key'])
            for collection in ('poi_localizations', 'geofence_zones', 'audio_tasks', 'audio_assets'):
                db[collection].delete_many({'poi_id': poi})
            db.poi.delete_one({'_id': poi})
        db.audio_assets.delete_many({'package_id': {'$in': package_ids}})
        db.audio_packages.delete_many({'_id': {'$in': package_ids}})
        db.admin_users.delete_one({'_id': uid})
        mongo.close()


if __name__ == '__main__':
    main()
