"""Shared content revisions for browser-assisted, administrator-reviewed translations."""
import hashlib
import json


LANGUAGES = ('vi', 'en', 'fr', 'zh-Hans', 'ja', 'ko')
PROVIDER = 'chrome-translator'


def content_hash(title: str, description: str) -> str:
    return hashlib.sha256(json.dumps([title, description], ensure_ascii=False).encode()).hexdigest()


def revision(document: dict | None) -> str | None:
    if document is None:
        return None
    return hashlib.sha256(json.dumps([
        str(document['_id']), document.get('title'), document.get('description'),
        str(document.get('updated_at')),
    ], ensure_ascii=False).encode()).hexdigest()
