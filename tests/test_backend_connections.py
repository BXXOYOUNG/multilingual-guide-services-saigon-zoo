import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.config import MongoSettings, RedisSettings, load_settings
from backend.database import mongodb, redis_client


class SettingsTests(unittest.TestCase):
    def test_services_are_optional_when_unconfigured(self):
        settings = load_settings({})

        self.assertIsNone(settings.mongodb)
        self.assertIsNone(settings.redis)

    def test_mongodb_uri_and_database_must_be_set_together(self):
        with self.assertRaisesRegex(ValueError, "must be set together"):
            load_settings({"MONGODB_URI": "mongodb://localhost:27017"})

    def test_invalid_mongodb_uri_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "MONGODB_URI"):
            load_settings(
                {
                    "MONGODB_URI": "http://localhost:27017",
                    "MONGODB_DATABASE": "saigon_zoo",
                }
            )

    def test_invalid_redis_url_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "REDIS_URL"):
            load_settings({"REDIS_URL": "http://localhost:6379"})

    def test_empty_environment_value_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "REDIS_URL must not be empty"):
            load_settings({"REDIS_URL": "  "})

    def test_invalid_mongodb_database_name_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "MONGODB_DATABASE"):
            load_settings(
                {
                    "MONGODB_URI": "mongodb://localhost:27017",
                    "MONGODB_DATABASE": "invalid/name",
                }
            )

    def test_valid_service_settings_are_loaded(self):
        settings = load_settings(
            {
                "MONGODB_URI": "mongodb://localhost:27017",
                "MONGODB_DATABASE": "saigon_zoo",
                "REDIS_URL": "rediss://localhost:6379/0",
            }
        )

        self.assertEqual(
            settings.mongodb,
            MongoSettings(
                uri="mongodb://localhost:27017",
                database="saigon_zoo",
            ),
        )
        self.assertEqual(
            settings.redis,
            RedisSettings(url="rediss://localhost:6379/0"),
        )


class MongoConnectionTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await mongodb.close_mongodb()

    async def asyncTearDown(self):
        await mongodb.close_mongodb()

    async def test_connect_exposes_database_and_close_releases_client(self):
        database = object()
        client = MagicMock()
        client.admin.command = AsyncMock(return_value={"ok": 1})
        client.close = AsyncMock()
        client.__getitem__.return_value = database

        with patch("backend.database.mongodb.AsyncMongoClient", return_value=client):
            await mongodb.connect_mongodb(
                MongoSettings("mongodb://localhost:27017", "saigon_zoo")
            )

        self.assertIs(mongodb.get_database(), database)
        client.admin.command.assert_awaited_once_with("ping")

        await mongodb.close_mongodb()

        client.close.assert_awaited_once()
        with self.assertRaisesRegex(RuntimeError, "not configured"):
            mongodb.get_database()

    async def test_failed_ping_closes_client_and_does_not_publish_database(self):
        client = MagicMock()
        client.admin.command = AsyncMock(side_effect=ConnectionError("unavailable"))
        client.close = AsyncMock()

        with patch("backend.database.mongodb.AsyncMongoClient", return_value=client):
            with self.assertRaisesRegex(ConnectionError, "unavailable"):
                await mongodb.connect_mongodb(
                    MongoSettings("mongodb://localhost:27017", "saigon_zoo")
                )

        client.close.assert_awaited_once()
        with self.assertRaisesRegex(RuntimeError, "not configured"):
            mongodb.get_database()


class RedisConnectionTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await redis_client.close_redis()

    async def asyncTearDown(self):
        await redis_client.close_redis()

    async def test_connect_exposes_client_and_close_releases_it(self):
        client = MagicMock()
        client.ping = AsyncMock(return_value=True)
        client.aclose = AsyncMock()

        with patch(
            "backend.database.redis_client.Redis.from_url",
            return_value=client,
        ) as from_url:
            await redis_client.connect_redis(
                RedisSettings("redis://localhost:6379/0")
            )

        self.assertIs(redis_client.get_redis_client(), client)
        from_url.assert_called_once_with(
            "redis://localhost:6379/0",
            decode_responses=True,
        )
        client.ping.assert_awaited_once_with()

        await redis_client.close_redis()

        client.aclose.assert_awaited_once()
        with self.assertRaisesRegex(RuntimeError, "not configured"):
            redis_client.get_redis_client()

    async def test_failed_ping_closes_client_and_does_not_publish_it(self):
        client = MagicMock()
        client.ping = AsyncMock(side_effect=ConnectionError("unavailable"))
        client.aclose = AsyncMock()

        with patch(
            "backend.database.redis_client.Redis.from_url",
            return_value=client,
        ):
            with self.assertRaisesRegex(ConnectionError, "unavailable"):
                await redis_client.connect_redis(
                    RedisSettings("redis://localhost:6379/0")
                )

        client.aclose.assert_awaited_once()
        with self.assertRaisesRegex(RuntimeError, "not configured"):
            redis_client.get_redis_client()


if __name__ == "__main__":
    unittest.main()
