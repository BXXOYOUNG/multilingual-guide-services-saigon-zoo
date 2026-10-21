"""Restore a handoff into temporary Docker resources and verify its contents.

Does not modify the source database/storage. Temporary containers and the temporary
SeaweedFS volume are removed in finally. The original Docker images are retained.
"""
import argparse
import hashlib
import json
import secrets
import subprocess
import time
from pathlib import Path

import boto3


def run(*args):
    result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(f'{args[0]} {args[1]} failed (exit {result.returncode})')
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('backup', type=Path)
    args = parser.parse_args()
    backup = args.backup.resolve()
    metadata = json.loads((backup / 'backup-metadata.json').read_text(encoding='utf-8'))
    settings = dict(line.split('=', 1) for line in (backup / 'seaweed.env').read_text(encoding='utf-8').splitlines() if line)
    token = secrets.token_hex(5)
    mongo, storage, volume = ('tcv-verify-mongo-' + token, 'tcv-verify-storage-' + token, 'tcv-verify-data-' + token)
    try:
        run('docker', 'run', '-d', '--name', mongo, '--network', 'none', 'mongo:6.0')
        for _ in range(30):
            try:
                run('docker', 'exec', mongo, 'mongosh', '--quiet', '--eval', 'db.adminCommand({ping:1})')
                break
            except RuntimeError:
                time.sleep(1)
        else:
            raise RuntimeError('Temporary MongoDB did not start.')
        run('docker', 'cp', str(backup / 'database.archive.gz'), mongo + ':/tmp/database.archive.gz')
        run('docker', 'exec', mongo, 'mongorestore', '--gzip', '--archive=/tmp/database.archive.gz', '--nsInclude=saigon_zoo_tcv_dataset_dev.*')
        counts = json.loads(run('docker', 'exec', mongo, 'mongosh', 'saigon_zoo_tcv_dataset_dev', '--quiet', '--eval', 'JSON.stringify(Object.fromEntries(db.getCollectionNames().sort().map(n=>[n,db.getCollection(n).countDocuments({})])))'))
        if counts != metadata['collection_counts']:
            raise RuntimeError('Restored collection counts do not match the snapshot.')
        assets = json.loads(run('docker', 'exec', mongo, 'mongosh', 'saigon_zoo_tcv_dataset_dev', '--quiet', '--eval', 'JSON.stringify(db.audio_assets.find({},{_id:0,file_url:1,checksum:1,size_bytes:1}).toArray())'))
        print('Restored MongoDB counts match all snapshot collections.', flush=True)
        # Load the actual exported image rather than relying on a registry tag.
        run('docker', 'image', 'load', '-i', str(backup / 'seaweed-image.tar'))
        run('docker', 'volume', 'create', volume)
        run('docker', 'run', '--rm', '--mount', f'type=volume,source={volume},target=/restore', '--mount', f'type=bind,source={backup},target=/backup,readonly', 'alpine:3.20', 'tar', 'xzf', '/backup/seaweed-data.tar.gz', '-C', '/restore', '.')
        run('docker', 'run', '-d', '--name', storage, '-p', '127.0.0.1::8333', '--env-file', str(backup / 'seaweed.env'), '-v', volume + ':/data', metadata['seaweed_image'], 'mini', '-dir=/data')
        port = run('docker', 'port', storage, '8333/tcp').strip().rsplit(':', 1)[1]
        s3 = boto3.client('s3', endpoint_url='http://127.0.0.1:' + port, aws_access_key_id=settings['AWS_ACCESS_KEY_ID'], aws_secret_access_key=settings['AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
        for _ in range(45):
            try:
                s3.head_bucket(Bucket=settings['S3_BUCKET'])
                break
            except Exception:
                time.sleep(1)
        else:
            raise RuntimeError('Restored storage did not become available.')
        for asset in assets:
            response = s3.get_object(Bucket=settings['S3_BUCKET'], Key=asset['file_url'])
            stream = response['Body']
            try:
                data = stream.read()
            finally:
                stream.close()
            if len(data) != asset['size_bytes'] or hashlib.sha256(data).hexdigest() != asset['checksum']:
                raise RuntimeError('Restored audio integrity check failed.')
        report = {'mongodb_restore': 'passed', 'collection_counts': counts, 'seaweedfs_restore': 'passed', 'audio_sha256_verified': len(assets), 'verification': 'isolated temporary Docker resources, source volumes untouched'}
        (backup / 'RESTORE_VERIFICATION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print('Restored SeaweedFS verified: ' + str(len(assets)) + ' audio files, sizes and SHA-256 match.', flush=True)
    finally:
        for name in [mongo, storage]:
            subprocess.run(['docker', 'rm', '-f', '-v', name], capture_output=True)
        # Only this randomly named, newly created verification volume is removed.
        subprocess.run(['docker', 'volume', 'rm', volume], capture_output=True)


if __name__ == '__main__':
    main()
