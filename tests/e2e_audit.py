"""Opt-in browser audit against a running local demo; never uses a real admin password.

Creates and removes a temporary admin. Visitor analytics are intercepted so these
checks do not inflate the live dashboard. Run manually, not through pytest.
"""
import json
import os
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pymongo import MongoClient
from playwright.sync_api import sync_playwright, expect
from backend.services.admin_auth import hash_password


def main():
    out = ROOT / '.demo-run/audit'
    out.mkdir(parents=True, exist_ok=True)
    checks, page_errors, events = [], [], []
    base = 'http://localhost:3000'
    mongo = MongoClient('mongodb://127.0.0.1:27018/?replicaSet=rs0')
    db = mongo['saigon_zoo_tcv_dataset_dev']
    username, password = 'audit-' + secrets.token_hex(6), secrets.token_urlsafe(24)
    role = db.roles.find_one({'name': 'administrator'})
    uid = db.admin_users.insert_one({'username': username, 'email': username + '@localhost.invalid', 'password_hash': hash_password(password), 'role_id': role['_id'], 'is_active': True, 'created_at': datetime.now(timezone.utc)}).inserted_id
    temporary_pois = []
    try:
        with sync_playwright() as pw:
            chromium = next((Path(os.environ['LOCALAPPDATA']) / 'ms-playwright').glob('chromium-*/chrome-win64/chrome.exe'))
            browser = pw.chromium.launch(executable_path=str(chromium), headless=True, args=['--autoplay-policy=no-user-gesture-required'])
            context = browser.new_context(viewport={'width': 1440, 'height': 1000}, permissions=['geolocation'], geolocation={'latitude': 10.85, 'longitude': 106.76})
            context.add_init_script("localStorage.setItem('saigon_zoo_selected_language', 'vi')")
            def intercept(route):
                events.append(route.request.post_data_json)
                route.fulfill(status=202, json={'accepted': True})
            context.route('**/api/analytics/events', intercept)
            page = context.new_page()
            page.set_default_navigation_timeout(15000)
            page.on('pageerror', lambda error: page_errors.append(str(error)))
            page.goto(base)
            expect(page.locator('.species-gallery .species-row')).to_have_count(11)
            page.locator('.species-gallery').scroll_into_view_if_needed()
            page.wait_for_function("Array.from(document.querySelectorAll('.species-photo img')).every(i => i.complete && i.naturalWidth > 0)")
            checks.append('11 catalog images load')
            print('PASS catalog images', flush=True)
            page.screenshot(path=str(out / 'home-desktop.png'), full_page=True)
            for size in [(390,844), (768,1024), (1440,1000)]:
                page.set_viewport_size({'width':size[0], 'height':size[1]})
                for path in ['/', '/map', '/explore', '/itinerary', '/guide', '/admin']:
                    page.goto(base+path)
                    page.wait_for_timeout(600)
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2'), (size,path,'horizontal overflow')
                    assert 'Unexpected Application Error' not in page.locator('body').inner_text()
                checks.append(f'Routes/no horizontal overflow {size[0]}px')
                print(f'PASS routes {size[0]}px', flush=True)
            # Login and dialog interaction on desktop and a narrow viewport.
            page.goto(base+'/admin')
            page.locator('input[autocomplete=username]').fill(username)
            page.locator('input[autocomplete=current-password]').fill(password)
            page.locator('.admin-login button[type=submit], .admin-login form button').click()
            expect(page.locator('.admin-poi-row')).to_have_count(11, timeout=30000)
            page.locator('.admin-search input').fill('no-such-animal-123')
            expect(page.locator('.admin-poi-row')).to_have_count(0)
            page.locator('.admin-search input').fill('')
            page.get_by_role('button', name='Sửa POI', exact=True).first.click()
            expect(page.locator('dialog[open]')).to_be_visible()
            assert page.locator('dialog input').first.input_value()
            page.keyboard.press('Escape')
            expect(page.locator('dialog[open]')).to_have_count(0)
            page.screenshot(path=str(out/'admin-desktop.png'), full_page=True)
            page.set_viewport_size({'width':390,'height':844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2')
            page.screenshot(path=str(out/'admin-mobile.png'), full_page=True)
            page.goto(base+'/admin/analytics')
            expect(page.locator('.dashboard-kpi')).to_have_count(5, timeout=30000)
            checks.append('Admin login, search, editor dialog, dashboard')
            payload = {'name': username, 'category': 'audit', 'description': 'Temporary audit POI', 'latitude': 10.788, 'longitude': 106.706, 'is_active': True}
            created = context.request.post(base+'/api/admin/pois', data=payload)
            assert created.status == 201, created.text()
            poi_id = created.json()['id']
            temporary_pois.append(poi_id)
            localized = context.request.put(base+f'/api/admin/pois/{poi_id}/localizations/vi', data={'title': username, 'description': 'Temporary audit translation', 'tts_status': 'draft'})
            assert localized.ok, localized.text()
            assert any(row['id'] == poi_id for row in context.request.get(base+'/api/pois?language=vi').json())
            updated = context.request.put(base+f'/api/admin/pois/{poi_id}', data={**payload, 'latitude':10.789})
            assert updated.ok, updated.text()
            hidden = context.request.delete(base+f'/api/admin/pois/{poi_id}')
            assert hidden.ok
            assert not any(row['id'] == poi_id for row in context.request.get(base+'/api/pois?language=vi').json())
            checks.append('Admin API create, localize, update and hide a disposable POI')
            print('PASS admin UI and temporary CRUD', flush=True)
            # All six packages must survive offline navigation and language changes.
            for pack in db.audio_packages.find({}):
                page.goto(base+f"/explore?package={pack['_id']}")
                page.wait_for_function("!location.search", timeout=90000)
            expect(page.locator('.explore-page .card').nth(1).locator('.offline-package-row')).to_have_count(6)
            page.evaluate('navigator.serviceWorker.ready')
            page.goto(base+'/map')  # load lazy map chunk before going offline
            expect(page.locator('.map-poi-marker')).to_have_count(11)
            page.locator('.map-demo-geofence button').click()
            page.locator('.map-poi-marker').first.click()
            expect(page.locator('.poi-audio-player')).to_be_visible()
            page.locator('.map-simulate-button').click()
            page.wait_for_function("document.querySelector('[role=status]')?.textContent?.includes('Đang phát')", timeout=15000)
            page.goto(base+'/explore')
            checks.append('Map simulation opens and starts audio')
            print('PASS packages and map simulation', flush=True)
            context.set_offline(True)
            for language in ['Tiếng Việt', 'English', 'Français', '简体中文', '日本語', '한국어']:
                page.goto(base+'/explore')
                page.locator('.language-chip').click()
                page.locator('.language-option').filter(has=page.get_by_text(language, exact=True)).click()
                rows = page.locator('.explore-page .card').nth(2).locator('.offline-package-row')
                expect(rows).to_have_count(11)
                rows.first.locator('button').click()
                page.wait_for_function("document.querySelector('audio').currentTime > 0", timeout=20000)
                page.goto(base+'/map')
                expect(page.locator('.map-poi-marker')).to_have_count(11)
                page.locator('.map-poi-marker').first.click()
                expect(page.locator('.poi-audio-player')).to_be_visible()
                print('PASS offline language', ascii(language), flush=True)
            checks.append('6 packages, 66 recordings, offline playback and POI map in 6 languages')
            context.set_offline(False)
            page.goto(base+'/admin')
            # Explicit logout removes the temporary account's Redis session.
            context.request.post(base+'/api/admin/auth/logout')
            browser.close()
        assert not page_errors, page_errors
        report={'passed':checks,'page_errors':page_errors,'intercepted_analytics_events':len(events)}
        (out/'browser-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(report,ensure_ascii=True,indent=2))
    finally:
        from bson import ObjectId
        for poi_id in temporary_pois:
            db.poi_localizations.delete_many({'poi_id': ObjectId(poi_id)})
            db.poi.delete_one({'_id': ObjectId(poi_id)})
        db.admin_users.delete_one({'_id':uid})
        mongo.close()


if __name__ == '__main__':
    main()
