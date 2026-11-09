// Native on-device translation only. No cloud fallback or third-party translation request.
export function hasBrowserTranslation() {
  return globalThis.isSecureContext && typeof globalThis.Translator?.create === 'function'
    && typeof globalThis.Translator?.availability === 'function';
}

function pair(source, target) {
  const code = (language) => language === 'zh-Hans' ? 'zh' : language;
  return { sourceLanguage: code(source), targetLanguage: code(target) };
}

export async function translationAvailability(source, target) {
  if (!hasBrowserTranslation()) return 'unavailable';
  return globalThis.Translator.availability(pair(source, target));
}

function contentError() {
  const error = new Error('Translation output exceeds content limits.');
  error.name = 'TranslationContentError';
  return error;
}

// Keep chunks small to avoid exceeding native input quotas with a long narration.
function chunks(line) {
  const result = [];
  let remaining = Array.from(line);
  while (remaining.length > 1000) {
    const sample = remaining.slice(0, 1000).join('');
    const boundary = Math.max(sample.lastIndexOf(' '), sample.lastIndexOf('。'), sample.lastIndexOf('. '));
    const length = boundary > 500 ? Array.from(sample.slice(0, boundary + 1)).length : 1000;
    result.push(remaining.slice(0, length).join(''));
    remaining = remaining.slice(length);
  }
  if (remaining.length) result.push(remaining.join(''));
  return result;
}

// Invoke directly from the button handler: create() must begin during user activation,
// before waiting on fetch, availability(), or another language's download.
export function startBrowserTranslation({ source, target, title, description, signal, onProgress }) {
  if (!hasBrowserTranslation()) throw new DOMException('Translator API unavailable', 'NotSupportedError');
  const creating = globalThis.Translator.create({ ...pair(source, target), signal,
    monitor(monitor) {
      monitor.addEventListener('downloadprogress', (event) => onProgress?.({ phase: 'downloading',
        progress: Math.round(Math.max(0, Math.min(1, event.loaded)) * 100) }));
    },
  });
  return (async () => {
    let translator;
    try {
      translator = await creating;
      signal.throwIfAborted();
      onProgress?.({ phase: 'translating' });
      const translatedTitle = (await translator.translate(title, { signal })).trim();
      const lines = [];
      for (const line of description.split('\n')) {
        if (!line.trim()) { lines.push(line); continue; }
        const parts = [];
        for (const chunk of chunks(line)) {
          signal.throwIfAborted();
          if (chunk.trim()) {
            const translated = (await translator.translate(chunk, { signal })).trim();
            if (!translated) throw contentError();
            parts.push(translated);
          }
        }
        lines.push(parts.join(' '));
      }
      const translatedDescription = lines.join('\n').trim();
      if (!translatedTitle || !translatedDescription || translatedTitle.length > 180 || translatedDescription.length > 10000) throw contentError();
      return { title: translatedTitle, description: translatedDescription };
    } finally { translator?.destroy(); }
  })();
}

export function translationErrorKey(error) {
  return ({ NotSupportedError: 'pairUnavailable', NotAllowedError: 'activation',
    QuotaExceededError: 'quota', TranslationContentError: 'contentLimit',
    AbortError: 'cancelled', TimeoutError: 'timeout' })[error.name] || 'failed';
}
