"""Prepare private MongoDB/SeaweedFS backups. Stop the backend before running.

The output directory must be outside this repository. No credentials are printed.
The storage container is briefly stopped for its volume snapshot and restarted.
"""
import argparse
import json
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from pymongo import MongoClient

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        # Never dump docker inspect/environment output on failure.
        raise RuntimeError(f'{args[0]} {args[1]} failed (exit {result.returncode})')
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error('Private backups must be outside the source repository.')
    if output.exists():
        parser.error('Choose a new output directory, not an existing backup.')
    with socket.socket() as sock:
        sock.settimeout(1)
        if sock.connect_ex(('127.0.0.1', 8000)) == 0:
            parser.error('Stop the backend on port 8000 before taking a consistent snapshot.')

    mongo = json.loads(run('docker', 'inspect', 'saigon-zoo-t10-replset'))[0]
    storage = json.loads(run('docker', 'inspect', 'saigon-zoo-t10-seaweedfs'))[0]
    if mongo['State']['Status'] != 'running' or storage['State']['Status'] != 'running':
        parser.error('MongoDB and SeaweedFS must be running before backup starts.')
    volume = next(m['Name'] for m in storage['Mounts'] if m['Destination'] == '/data' and m['Type'] == 'volume')
    settings = {k: v for entry in storage['Config']['Env'] for k, v in [entry.split('=', 1)] if k in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'S3_BUCKET']}
    if len(settings) != 3 or any(not value or '\n' in value or '\r' in value for value in settings.values()):
        parser.error('The storage environment is incomplete or cannot be exported safely.')
    run('docker', 'pull', 'alpine:3.20')
    output.mkdir(parents=True)
    (output / 'seaweed.env').write_text(''.join(f'{k}={v}\n' for k, v in settings.items()), encoding='utf-8')
    now = datetime.now(timezone.utc)
    with MongoClient('mongodb://127.0.0.1:27018/?replicaSet=rs0', serverSelectionTimeoutMS=5000) as client:
        db = client['saigon_zoo_tcv_dataset_dev']
        counts = {name: db[name].count_documents({}) for name in sorted(db.list_collection_names())}
    archive_path = '/tmp/tcv-handoff-' + now.strftime('%Y%m%d%H%M%S') + '.archive.gz'
    run('docker', 'exec', 'saigon-zoo-t10-replset', 'mongodump', '--host', '127.0.0.1', '--port', '27018', '--db', 'saigon_zoo_tcv_dataset_dev', '--gzip', '--archive=' + archive_path)
    run('docker', 'cp', 'saigon-zoo-t10-replset:' + archive_path, str(output / 'database.archive.gz'))
    print('MongoDB snapshot complete.', flush=True)
    run('docker', 'stop', 'saigon-zoo-t10-seaweedfs')
    try:
        run('docker', 'run', '--rm', '--mount', f'type=volume,source={volume},target=/source,readonly', '--mount', f'type=bind,source={output},target=/backup', 'alpine:3.20', 'tar', 'czf', '/backup/seaweed-data.tar.gz', '-C', '/source', '.')
    finally:
        run('docker', 'start', 'saigon-zoo-t10-seaweedfs')
    print('SeaweedFS volume snapshot complete; original storage restarted.', flush=True)
    image_tag = 'saigon-zoo-handoff/seaweedfs:' + now.strftime('%Y%m%d')
    run('docker', 'image', 'tag', storage['Image'], image_tag)
    run('docker', 'image', 'save', '-o', str(output / 'seaweed-image.tar'), image_tag)
    metadata = {'created_at_utc': now.isoformat(), 'database': 'saigon_zoo_tcv_dataset_dev', 'collection_counts': counts, 'seaweed_image': image_tag, 'seaweed_image_id': storage['Image'], 'source_branch': run('git', '-C', str(ROOT), 'branch', '--show-current').strip(), 'source_base_commit': run('git', '-C', str(ROOT), 'rev-parse', 'HEAD').strip(), 'source_note': 'Includes uncommitted staged changes when source.zip is added; see SOURCE_STATE.txt.'}
    (output / 'backup-metadata.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    print('Backup files prepared at: ' + str(output), flush=True)


if __name__ == '__main__':
    main()
