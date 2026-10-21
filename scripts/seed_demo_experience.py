#!/usr/bin/env python3
"""Seed the explicitly simulated, full-featured classroom demo dataset.

Dry-run by default. --apply activates all 11 curated POIs and installs demo
geofences. --generate-audio creates six-language Edge TTS assets and uploads
them to the configured SeaweedFS S3 bucket. Generated voices are simulation
content and must stay labeled that way in the app.
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import boto3
from bson import ObjectId
from botocore.config import Config
from pymongo import MongoClient

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "dataset"
DATABASE = "saigon_zoo_tcv_dataset_dev"
MONGO_URI = "mongodb://127.0.0.1:27018/?replicaSet=rs0"
GEO = {
    "TCV-AN-001": (10.78845, 106.70595),
    "TCV-AN-002": (10.78845, 106.70655),
    "TCV-AN-003": (10.78845, 106.70715),
    "TCV-AN-004": (10.78800, 106.70595),
    "TCV-AN-005": (10.7886498, 106.7071674),
    "TCV-AN-006": (10.78800, 106.70655),
    "TCV-AN-007": (10.78800, 106.70715),
    "TCV-AN-008": (10.78755, 106.70595),
    "TCV-AN-009": (10.78755, 106.70655),
    "TCV-AN-010": (10.78755, 106.70715),
    "TCV-AN-011": (10.7880953, 106.7078014),
}
VOICES = {
    "vi": "vi-VN-HoaiMyNeural",
    "en": "en-US-AvaNeural",
    "fr": "fr-FR-VivienneMultilingualNeural",
    "zh-Hans": "zh-CN-XiaoxiaoNeural",
    "ja": "ja-JP-NanamiNeural",
    "ko": "ko-KR-SunHiNeural",
}
DEMO_PREFIX = {
    "vi": "Bản thuyết minh mô phỏng. ",
    "en": "Demo narration. ",
    "fr": "Narration de démonstration. ",
    "zh-Hans": "演示讲解。",
    "ja": "デモ用の音声ガイドです。",
    "ko": "시연용 오디오 해설입니다. ",
}


def rows(name: str) -> list[dict[str, str]]:
    with (DATASET / name).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def storage_config() -> dict[str, str]:
    names = {
        "AUDIO_STORAGE_BUCKET": "S3_BUCKET",
        "AUDIO_STORAGE_ACCESS_KEY_ID": "AWS_ACCESS_KEY_ID",
        "AUDIO_STORAGE_SECRET_ACCESS_KEY": "AWS_SECRET_ACCESS_KEY",
    }
    config = {key: os.getenv(key, "").strip() for key in names}
    if not all(config.values()):
        inspect = json.loads(subprocess.check_output(
            ["docker", "inspect", "saigon-zoo-t10-seaweedfs"], text=True
        ))[0]
        env = inspect["Config"].get("Env", [])
        for target, source in names.items():
            if not config[target]:
                config[target] = next(
                    (item.split("=", 1)[1] for item in env if item.startswith(source + "=")), ""
                )
    if not all(config.values()):
        raise RuntimeError("SeaweedFS S3 credentials/bucket are not configured")
    config["AUDIO_STORAGE_ENDPOINT_URL"] = os.getenv(
        "AUDIO_STORAGE_ENDPOINT_URL", "http://127.0.0.1:8333"
    )
    return config


def install_demo_content(database: Any, candidates: list[dict[str, str]], localizations: list[dict[str, str]]) -> dict[str, ObjectId]:
    image_credits = json.loads((DATASET / "demo_image_credits.json").read_text(encoding="utf-8"))
    titles = {
        row["title"]: row["poi_id"]
        for row in database["poi_localizations"].find(
            {"language_code": "vi"}, {"poi_id": 1, "title": 1}
        )
    }
    poi_ids: dict[str, ObjectId] = {}
    by_code = {row["candidate_code"]: row for row in candidates}
    now = datetime.now(timezone.utc)
    for code, candidate in by_code.items():
        poi_id = titles.get(candidate["name_vi"])
        if poi_id is None:
            raise RuntimeError(f"Missing POI localization for {code}")
        poi_ids[code] = poi_id
        lat, lon = GEO[code]
        database["poi"].update_one({"_id": poi_id}, {"$set": {
            "candidate_code": code,
            "name": candidate["name_vi"],
            "category": "animal_exhibit",
            "scientific_name": candidate["scientific_name"],
            "source_url": candidate["species_source_url"],
            "image_url": image_credits[code]["local_path"],
            "image_source_url": image_credits[code]["file_page"],
            "image_license": image_credits[code]["license"],
            "latitude": lat,
            "longitude": lon,
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "coordinate_source": "Simulated exhibit coordinate for classroom demo",
            "coordinate_source_url": candidate.get("coordinate_source_url") or candidate["map_reference_url"],
            "coordinate_status": "DEMO_APPROXIMATE_NOT_VERIFIED",
            "data_status": "DEMO_CONTENT_DRAFT",
            "is_demo": True,
            "is_active": True,
            "geofence_enabled": True,
            "updated_at": now,
        }})

    for loc in localizations:
        poi_id = poi_ids[loc["candidate_code"]]
        previous = database["poi_localizations"].find_one({"poi_id": poi_id, "language_code": loc["language_code"]})
        changed = previous is None or previous.get("title") != loc["title"] or previous.get("description") != loc["description"]
        audio_fields = {"audio_url": None, "audio_status": "DEMO_TTS_PENDING", "tts_status": "draft"} if changed else {}
        if loc["language_code"] == "vi":
            database["poi"].update_one({"_id": poi_id}, {"$set": {"description": loc["description"]}})
        database["poi_localizations"].update_one(
            {"poi_id": poi_id, "language_code": loc["language_code"]},
            {"$set": {
                "title": loc["title"],
                "description": loc["description"],
                "content_status": "DEMO_DRAFT",
                "fact_review_status": "DEMO_NOT_FOR_PRODUCTION",
                "translation_review_status": "DEMO_TRANSLATION_NOT_REVIEWED",
                **audio_fields,
                "is_demo": True,
                "source_url": loc["source_url"],
                "updated_at": now,
            }},
            upsert=True,
        )

    for code, poi_id in poi_ids.items():
        lat, lon = GEO[code]
        database["geofence_zones"].update_one(
            {"poi_id": poi_id, "is_demo": True},
            {"$set": {
                "poi_id": poi_id,
                "zone_type": "circle",
                "radius": 35,
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "is_active": True,
                "is_demo": True,
                "demo_notice": "Approximate classroom simulation; not an on-site survey.",
                "updated_at": now,
            }, "$setOnInsert": {"created_at": now}},
            upsert=True,
        )
    return poi_ids


async def generate_audio(database: Any, poi_ids: dict[str, ObjectId], localizations: list[dict[str, str]]) -> int:
    import edge_tts

    config = storage_config()
    s3 = boto3.client(
        "s3",
        endpoint_url=config["AUDIO_STORAGE_ENDPOINT_URL"],
        region_name=os.getenv("AUDIO_STORAGE_REGION", "us-east-1"),
        aws_access_key_id=config["AUDIO_STORAGE_ACCESS_KEY_ID"],
        aws_secret_access_key=config["AUDIO_STORAGE_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    )
    bucket = config["AUDIO_STORAGE_BUCKET"]
    now = datetime.now(timezone.utc)
    completed = 0
    for loc in localizations:
        code = loc["candidate_code"]
        language = loc["language_code"]
        poi_id = poi_ids[code]
        voice = VOICES[language]
        text = DEMO_PREFIX[language] + loc["description"]
        communicator = edge_tts.Communicate(text, voice)
        chunks: list[bytes] = []
        async for event in communicator.stream():
            if event["type"] == "audio":
                chunks.append(event["data"])
        audio = b"".join(chunks)
        if not audio.startswith(b"\xff") or len(audio) < 1024:
            raise RuntimeError(f"TTS returned an invalid audio stream for {code}/{language}")
        checksum = hashlib.sha256(audio).hexdigest()
        key = f"demo/poi/{code}/{language}.mp3"
        s3.put_object(
            Bucket=bucket, Key=key, Body=audio, ContentType="audio/mpeg",
            Metadata={"sha256": checksum, "demo": "true", "voice": voice},
        )
        word_count = max(1, len(text.split()))
        duration = round(word_count * 60 / 145, 2)
        database["audio_assets"].update_one(
            {"poi_id": poi_id, "language_code": language, "is_demo": True},
            {"$set": {
                "poi_id": poi_id,
                "language_code": language,
                "file_url": key,
                "duration": duration,
                "checksum": checksum,
                "size_bytes": len(audio),
                "is_demo": True,
                "voice": voice,
                "created_at": now,
            }, "$setOnInsert": {"package_id": None}},
            upsert=True,
        )
        database["poi_localizations"].update_one(
            {"poi_id": poi_id, "language_code": language},
            {"$set": {"audio_url": key, "audio_status": "DEMO_TTS_READY", "tts_status": "Completed", "is_demo": True}},
        )
        database["audio_tasks"].update_one(
            {"poi_id": poi_id, "language_code": language, "is_demo": True},
            {"$set": {
                "poi_id": poi_id, "language_code": language, "type": "TTS",
                "status": "Completed", "file_url": key, "voice": voice,
                "is_demo": True, "updated_at": now,
            }, "$setOnInsert": {"created_at": now}},
            upsert=True,
        )
        completed += 1
        print(f"audio ready: {code} / {language} ({len(audio)} bytes)")
    return completed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write simulated data and geofences to dev MongoDB")
    parser.add_argument("--generate-audio", action="store_true", help="synthesize and upload all 66 six-language demo recordings")
    parser.add_argument("--database", default=DATABASE)
    parser.add_argument("--mongo-uri", default=MONGO_URI)
    args = parser.parse_args()
    if args.database != DATABASE:
        parser.error(f"This script is restricted to {DATABASE!r}.")
    candidates = rows("poi_candidates.csv")
    localizations = rows("poi_localizations_multilingual_v2.csv")
    if len(candidates) != 11 or len(localizations) != 66:
        parser.error("Expected 11 POIs and 66 localizations.")
    if not args.apply and not args.generate_audio:
        print("Dry run: 11 active demo POIs, 11 approximate geofences, 66 localized narratives.")
        print("Pass --apply to write simulated content; add --generate-audio for 66 Edge TTS recordings.")
        return 0
    client = MongoClient(args.mongo_uri, serverSelectionTimeoutMS=5000)
    try:
        database = client[args.database]
        poi_ids = {
            row["candidate_code"]: database["poi_localizations"].find_one(
                {"language_code": "vi", "title": row["name_vi"]}, {"poi_id": 1}
            )["poi_id"]
            for row in candidates
        }
        if args.apply:
            poi_ids = install_demo_content(database, candidates, localizations)
            print("Installed 11 simulated POIs, 66 localized narratives, and 11 approximate geofences.")
        if args.generate_audio:
            if not args.apply and database["poi"].count_documents({"is_demo": True}) != 11:
                raise RuntimeError("Apply demo content first with --apply --generate-audio")
            count = asyncio.run(generate_audio(database, poi_ids, localizations))
            print(f"Generated and uploaded {count} demo audio assets.")
        print({
            "demo_pois": database["poi"].count_documents({"is_demo": True}),
            "active_demo_pois": database["poi"].count_documents({"is_demo": True, "is_active": True}),
            "demo_geofences": database["geofence_zones"].count_documents({"is_demo": True, "is_active": True}),
            "demo_audio_assets": database["audio_assets"].count_documents({"is_demo": True}),
        })
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
