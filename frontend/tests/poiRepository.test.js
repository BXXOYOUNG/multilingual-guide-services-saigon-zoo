import assert from 'node:assert/strict';
import test from 'node:test';

import { fetchPois, PoiApiError } from '../src/services/poiRepository.js';

test('fetchPois requests the selected language and returns POIs', async () => {
  let requestedUrl;
  const pois = [
    {
      id: 'poi-1',
      name: 'Entrance',
      description: 'Main entrance',
      latitude: 10.78,
      longitude: 106.7,
    },
  ];

  const result = await fetchPois('vi-VN', async (url) => {
    requestedUrl = url;
    return new Response(JSON.stringify(pois), { status: 200 });
  });

  assert.equal(requestedUrl, '/api/pois?language=vi-VN');
  assert.deepEqual(result, pois);
});

test('fetchPois reports structured HTTP errors', async () => {
  await assert.rejects(
    fetchPois('vi', async () => new Response(JSON.stringify({
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'An unexpected error occurred',
        details: [],
      },
    }), { status: 500 })),
    (error) => {
      assert.ok(error instanceof PoiApiError);
      assert.equal(error.status, 500);
      assert.equal(error.code, 'INTERNAL_SERVER_ERROR');
      assert.equal(error.message, 'An unexpected error occurred');
      return true;
    },
  );
});

test('fetchPois propagates network failures', async () => {
  const networkError = new TypeError('Network unavailable');

  await assert.rejects(
    fetchPois('vi', async () => {
      throw networkError;
    }),
    networkError,
  );
});

test('fetchPois rejects a response that does not match the contract', async () => {
  await assert.rejects(
    fetchPois('vi', async () => new Response(JSON.stringify([{ id: 'missing-fields' }]))),
    /does not match the expected schema/,
  );
});
