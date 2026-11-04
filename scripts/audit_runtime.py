"""Read-only audit of the local demo database, API, image files and audio bytes.

Run from the repository root: .venv/Scripts/python.exe scripts/audit_runtime.py
Does not create accounts, rewrite data, seed, or expose storage credentials.
"""
import hashlib
import json
import os
from pathlib import Path
from urllib.request import urlopen

from bson import ObjectId
from pymongo import MongoClient

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ['vi', 'en', 'fr', 'zh-Hans', 'ja', 'ko']
API = os.getenv('AUDIT_API_URL', 'http://127.0.0.1:8000')


def main():
    errors, checks = [], []

    def check(ok, label):
        (checks if ok else errors).append(label)

    def request(path):
        with urlopen(API + path, timeout=30) as response:
            return json.load(response)

    with MongoClient(os.getenv('MONGODB_URI', 'mongodb://127.0.0.1:27018/?replicaSet=rs0'), serverSelectionTimeoutMS=5000) as client:
        db = client['saigon_zoo_tcv_dataset_dev']
        pois = list(db.poi.find({}))
        ids = {p['_id'] for p in pois}
        assets = list(db.audio_assets.find({}))
        packs = list(db.audio_packages.find({}))
        pack_by_id = {p['_id']: p for p in packs}
        for poi in pois:
            check(all(poi.get(k) for k in ['name', 'description', 'category']), f"POI metadata {poi['_id']}")
            check(poi.get('geometry', {}).get('coordinates') == [poi.get('longitude'), poi.get('latitude')], f"POI coordinates {poi['_id']}")
            image_url = poi.get('image_url', '')
            if image_url.startswith('/api/media/pois/'):
                with urlopen(API + image_url, timeout=30) as response:
                    check(response.headers.get_content_type().startswith('image/') and bool(response.read()), f"Uploaded image {poi['_id']}")
            elif image_url.startswith('/images/'):
                image = ROOT / 'frontend/public' / image_url.lstrip('/')
                check(image.is_file() and image.stat().st_size > 1000, f"Image file {poi['_id']}")
            elif image_url:
                check(image_url.startswith('https://'), f"External image URL {poi['_id']}")
        for language in LANGUAGES:
            rows = request('/api/pois?language=' + language)
            expected = {str(p['_id']) for p in pois if p.get('is_active') and db.poi_localizations.find_one({'poi_id': p['_id'], 'language_code': language})}
            check({p['id'] for p in rows} == expected, f'API POIs {language}')
            check(all(ObjectId.is_valid(p['id']) for p in rows), f'API ObjectIds {language}')
        for loc in db.poi_localizations.find({'audio_url': {'$nin': [None, '']}}):
            if not loc.get('audio_url'):
                continue
            resolved = request(f"/audio/assets/resolve?poi_id={loc['poi_id']}&language_code={loc['language_code']}")
            check(resolved['file_url'] == loc['audio_url'], f"Current audio resolution {loc['poi_id']}/{loc['language_code']}")
        for name in ['poi_localizations', 'audio_tasks', 'audio_assets', 'geofence_zones']:
            check(all(isinstance(d.get('poi_id'), ObjectId) and d['poi_id'] in ids for d in db[name].find({})), f'{name} POI references')
        check(all(isinstance(d.get('user_id'), ObjectId) for d in db.analytics_sessions.find({})), 'Session visitor ObjectIds')
        for asset in assets:
            key = f"{asset['poi_id']}/{asset['language_code']}"
            package = pack_by_id.get(asset.get('package_id'))
            check(not asset.get('package_id') or bool(package and package['language_code'] == asset['language_code']), f'Package language {key}')
            with urlopen(API + f"/audio/assets/{asset['_id']}/content", timeout=30) as response:
                data = response.read()
            check(hashlib.sha256(data).hexdigest() == asset['checksum'], f'Audio SHA256 {key}')
            check(len(data) == asset.get('size_bytes'), f'Audio size {key}')
        for pack in packs:
            manifest = request(f"/audio/packages/{pack['_id']}/manifest")
            check(manifest['integrity_status'] == 'verified', f"Manifest integrity {pack['language_code']}")
            check(len(manifest['assets']) == db.audio_assets.count_documents({'package_id': pack['_id']}), f"Manifest count {pack['_id']}")
        report = {'checks_passed': len(checks), 'errors': errors, 'counts': {'pois': len(pois), 'assets': len(assets), 'packages': len(packs)}}
        print(json.dumps(report, indent=2))
        return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
