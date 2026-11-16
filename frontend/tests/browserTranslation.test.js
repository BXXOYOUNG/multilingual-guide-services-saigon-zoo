import assert from 'node:assert/strict';
import test from 'node:test';
import { startBrowserTranslations } from '../src/services/browserTranslation.js';

function mockTranslator(t, create) {
  const secure = Object.getOwnPropertyDescriptor(globalThis, 'isSecureContext');
  const translator = Object.getOwnPropertyDescriptor(globalThis, 'Translator');
  Object.defineProperty(globalThis, 'isSecureContext', { configurable: true, value: true });
  Object.defineProperty(globalThis, 'Translator', { configurable: true, value: { create, availability() {} } });
  t.after(() => {
    if (secure) Object.defineProperty(globalThis, 'isSecureContext', secure);
    else delete globalThis.isSecureContext;
    if (translator) Object.defineProperty(globalThis, 'Translator', translator);
    else delete globalThis.Translator;
  });
}

const input = { source: 'vi', targets: ['en', 'fr', 'zh-Hans', 'ja', 'ko'], title: 'Title', description: 'Narration' };

test('one action starts all five models before awaiting and preserves the source language', async (t) => {
  const calls = [];
  const destroyed = [];
  let clickActive = true;
  mockTranslator(t, ({ sourceLanguage, targetLanguage }) => {
    assert.equal(clickActive, true, 'model creation must stay in the click handler');
    calls.push([sourceLanguage, targetLanguage]);
    return Promise.resolve({
      translate: async (text) => `${targetLanguage}: ${text}`,
      destroy: () => destroyed.push(targetLanguage),
    });
  });
  const pending = startBrowserTranslations({ ...input, signal: new AbortController().signal });
  clickActive = false;
  assert.deepEqual(calls, ['en', 'fr', 'zh', 'ja', 'ko'].map((target) => ['vi', target]));
  const results = await pending;
  assert.equal(results.length, 5);
  assert.equal(results[2].language_code, 'zh-Hans');
  assert.equal(results[2].value.description, 'zh: Narration');
  assert.equal(destroyed.length, 5);
});

test('a failed model does not discard translations for other languages', async (t) => {
  mockTranslator(t, ({ targetLanguage }) => {
    if (targetLanguage === 'fr') throw new DOMException('Unsupported pair', 'NotSupportedError');
    return Promise.resolve({ translate: async (text) => text, destroy() {} });
  });
  const results = await startBrowserTranslations({ ...input, signal: new AbortController().signal });
  assert.equal(results.find((row) => row.language_code === 'fr').error, 'pairUnavailable');
  assert.equal(results.filter((row) => row.value).length, 4);
});

test('cancelling a batch aborts every pending model', async (t) => {
  mockTranslator(t, ({ signal }) => new Promise((resolve, reject) => {
    signal.addEventListener('abort', () => reject(signal.reason), { once: true });
  }));
  const controller = new AbortController();
  const pending = startBrowserTranslations({ ...input, signal: controller.signal });
  controller.abort();
  const results = await pending;
  assert.equal(results.length, 5);
  assert.ok(results.every((row) => row.error === 'cancelled'));
});
