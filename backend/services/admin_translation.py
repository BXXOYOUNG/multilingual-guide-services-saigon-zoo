"""Google Cloud Translation Basic adapter. Never log credentials/provider bodies."""
import hashlib
import html
import json
import os

import httpx


LANGUAGES = ('vi', 'en', 'fr', 'zh-Hans', 'ja', 'ko')


def content_hash(title: str, description: str) -> str:
    return hashlib.sha256(json.dumps([title, description], ensure_ascii=False).encode()).hexdigest()


def revision(document: dict | None) -> str | None:
    if document is None:
        return None
    return hashlib.sha256(json.dumps([
        str(document['_id']), document.get('title'), document.get('description'),
        str(document.get('updated_at')),
    ], ensure_ascii=False).encode()).hexdigest()


class TranslationError(Exception):
    pass


class GoogleTranslator:
    provider = 'google-cloud-basic-v2'

    def __init__(self):
        self.key = os.getenv('GOOGLE_TRANSLATE_API_KEY', '').strip()

    async def translate(self, client: httpx.AsyncClient, source: str, target: str,
                        title: str, description: str) -> dict:
        codes = {'zh-Hans': 'zh-CN'}
        try:
            response = await client.post(
                'https://translation.googleapis.com/language/translate/v2',
                headers={'X-Goog-Api-Key': self.key},
                json={'q': [title, description], 'source': codes.get(source, source),
                      'target': codes.get(target, target), 'format': 'text'},
            )
            if response.status_code in (401, 403):
                raise TranslationError('Translation credentials/API access rejected. Check backend configuration.')
            if response.status_code == 429:
                raise TranslationError('Translation quota exceeded. Retry later or check Google Cloud quota.')
            if response.is_error:
                raise TranslationError('Translation provider unavailable. Retry this language later.')
            rows = response.json()['data']['translations']
            values = [html.unescape(row['translatedText']).strip() for row in rows]
            if len(values) != 2 or not all(values) or len(values[0]) > 180 or len(values[1]) > 10000:
                raise TranslationError('Translation exceeds content limits or is empty. Shorten the source and retry.')
            return {'title': values[0], 'description': values[1]}
        except (httpx.HTTPError, ValueError, KeyError, TypeError) as error:
            raise TranslationError('Translation request failed. Check connectivity and retry.') from error
