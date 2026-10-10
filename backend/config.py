import os
from dataclasses import dataclass, field
from typing import AbstractSet, Mapping, Optional
from urllib.parse import urlsplit


@dataclass(frozen=True)
class MongoSettings:
    uri: str = field(repr=False)
    database: str


@dataclass(frozen=True)
class RedisSettings:
    url: str = field(repr=False)


@dataclass(frozen=True)
class Settings:
    mongodb: Optional[MongoSettings]
    redis: Optional[RedisSettings]


def _read_value(environment: Mapping[str, str], name: str) -> Optional[str]:
    value = environment.get(name)
    if value is None:
        return None
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
    return value.strip()


def _validate_url(value: str, name: str, schemes: AbstractSet[str]) -> None:
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        _ = parsed.port
    except ValueError as error:
        raise ValueError(f"{name} must be a valid URL") from error

    if parsed.scheme not in schemes or not hostname:
        allowed_schemes = ", ".join(sorted(schemes))
        raise ValueError(
            f"{name} must use one of these schemes and include a host: "
            f"{allowed_schemes}"
        )


def load_settings(environment: Optional[Mapping[str, str]] = None) -> Settings:
    values = os.environ if environment is None else environment
    mongodb_uri = _read_value(values, "MONGODB_URI")
    mongodb_database = _read_value(values, "MONGODB_DATABASE")
    redis_url = _read_value(values, "REDIS_URL")

    if (mongodb_uri is None) != (mongodb_database is None):
        raise ValueError("MONGODB_URI and MONGODB_DATABASE must be set together")

    mongodb = None
    if mongodb_uri is not None and mongodb_database is not None:
        _validate_url(
            mongodb_uri,
            "MONGODB_URI",
            {"mongodb", "mongodb+srv"},
        )
        if any(character in mongodb_database for character in '/\\."$<>:|?*'):
            raise ValueError("MONGODB_DATABASE contains an invalid character")
        mongodb = MongoSettings(uri=mongodb_uri, database=mongodb_database)

    redis = None
    if redis_url is not None:
        _validate_url(redis_url, "REDIS_URL", {"redis", "rediss"})
        redis = RedisSettings(url=redis_url)

    return Settings(mongodb=mongodb, redis=redis)
