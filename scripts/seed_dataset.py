#!/usr/bin/env python3
"""Safely seed the TCV student-project dataset into an isolated MongoDB dev DB.

The script defaults to dry-run and never connects to MongoDB unless --apply is set.
Only schema fields used by the current POI read API are written:
  poi: _id, latitude, longitude, is_active
  poi_localizations: poi_id, language_code, title, description

Approximate map pins require --allow-demo-coordinates. Activating draft POIs requires
both --allow-demo-coordinates and --allow-draft-content and should be dev-only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import sys
from dataclasses import dataclass
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "dataset"
DEFAULT_DATABASE = "saigon_zoo_tcv_dataset_dev"
DEFAULT_MONGO_URI = "mongodb://127.0.0.1:27018/?replicaSet=rs0"
REQUIRED_LANGUAGES = {"vi", "en", "fr", "zh-Hans", "ja", "ko"}


@dataclass(frozen=True)
class PlannedPOI:
    candidate_code: str
    poi_id: str
    latitude: float
    longitude: float
    coordinate_status: str
    is_active: bool


@dataclass(frozen=True)
class ImportPlan:
    pois: list[PlannedPOI]
    localizations: list[dict[str, Any]]
    skipped_candidates: list[tuple[str, str]]
    all_candidate_codes: list[str]
    languages: set[str]


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.is_file():
        raise ValueError(f"Required CSV not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {path}")
        rows = list(reader)
        return rows, list(reader.fieldnames)


def deterministic_poi_id(candidate_code: str) -> str:
    """Return a stable 24-hex id; converted to BSON ObjectId only while writing."""
    digest = hashlib.sha256(f"tcv-seed-v1:{candidate_code}".encode("utf-8")).hexdigest()
    return digest[:24]


def is_dev_database(database: str) -> bool:
    normalized = database.lower()
    return normalized.endswith(("_dev", "_test", "-dev", "-test"))


def parse_coordinate(value: str, field: str, candidate_code: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid {field} for {candidate_code}: {value!r}") from exc
    if field == "latitude" and not -90 <= number <= 90:
        raise ValueError(f"Latitude outside [-90, 90] for {candidate_code}: {number}")
    if field == "longitude" and not -180 <= number <= 180:
        raise ValueError(f"Longitude outside [-180, 180] for {candidate_code}: {number}")
    return number


def build_import_plan(
    data_dir: Path,
    *,
    allow_demo_coordinates: bool = False,
    activate_demo_pois: bool = False,
    allow_draft_content: bool = False,
) -> ImportPlan:
    if activate_demo_pois and not allow_demo_coordinates:
        raise ValueError("--activate-demo-pois requires --allow-demo-coordinates")
    if activate_demo_pois and not allow_draft_content:
        raise ValueError("--activate-demo-pois requires --allow-draft-content")

    candidates, candidate_fields = read_csv(data_dir / "poi_candidates.csv")
    localizations, localization_fields = read_csv(
        data_dir / "poi_localizations_multilingual_v2.csv"
    )
    languages_rows, language_fields = read_csv(data_dir / "language_manifest.csv")
    coordinate_rows, coordinate_fields = read_csv(data_dir / "poi_demo_coordinates.csv")

    required_candidate_fields = {"candidate_code", "latitude", "longitude", "is_active"}
    required_localization_fields = {
        "candidate_code", "language_code", "title", "description"
    }
    required_language_fields = {"language_code"}
    required_coordinate_fields = {"candidate_code", "latitude", "longitude", "coordinate_status"}
    for file_name, fields, required in [
        ("poi_candidates.csv", candidate_fields, required_candidate_fields),
        ("poi_localizations_multilingual_v2.csv", localization_fields, required_localization_fields),
        ("language_manifest.csv", language_fields, required_language_fields),
        ("poi_demo_coordinates.csv", coordinate_fields, required_coordinate_fields),
    ]:
        missing = sorted(required - set(fields))
        if missing:
            raise ValueError(f"{file_name} is missing columns: {', '.join(missing)}")

    candidate_by_code: dict[str, dict[str, str]] = {}
    for row in candidates:
        code = (row.get("candidate_code") or "").strip()
        if not code:
            raise ValueError("A POI row has an empty candidate_code")
        if code in candidate_by_code:
            raise ValueError(f"Duplicate POI candidate_code: {code}")
        candidate_by_code[code] = row
    if not candidate_by_code:
        raise ValueError("poi_candidates.csv contains no candidate rows")

    language_set = {(row.get("language_code") or "").strip() for row in languages_rows}
    language_set.discard("")
    if not REQUIRED_LANGUAGES.issubset(language_set):
        missing = sorted(REQUIRED_LANGUAGES - language_set)
        raise ValueError(f"language_manifest.csv is missing expected languages: {missing}")

    coordinate_by_code: dict[str, dict[str, str]] = {}
    for row in coordinate_rows:
        code = (row.get("candidate_code") or "").strip()
        if not code:
            raise ValueError("A coordinate row has an empty candidate_code")
        if code in coordinate_by_code:
            raise ValueError(f"Duplicate coordinate candidate_code: {code}")
        if code not in candidate_by_code:
            raise ValueError(f"Coordinate file references unknown POI candidate: {code}")
        coordinate_by_code[code] = row

    localization_by_key: dict[tuple[str, str], dict[str, str]] = {}
    localization_languages: dict[str, set[str]] = {}
    for row in localizations:
        code = (row.get("candidate_code") or "").strip()
        lang = (row.get("language_code") or "").strip()
        if code not in candidate_by_code:
            raise ValueError(f"Localization references unknown candidate_code: {code}")
        if lang not in language_set:
            raise ValueError(f"Localization uses language absent from manifest: {lang}")
        if not (row.get("title") or "").strip():
            raise ValueError(f"Empty title in localization: {code}/{lang}")
        if not (row.get("description") or "").strip():
            raise ValueError(f"Empty description in localization: {code}/{lang}")
        key = (code, lang)
        if key in localization_by_key:
            raise ValueError(f"Duplicate localization row: {code}/{lang}")
        localization_by_key[key] = row
        localization_languages.setdefault(code, set()).add(lang)

    for code in candidate_by_code:
        missing_languages = REQUIRED_LANGUAGES - localization_languages.get(code, set())
        if missing_languages:
            raise ValueError(f"{code} lacks localization languages: {sorted(missing_languages)}")

    planned_pois: list[PlannedPOI] = []
    skipped: list[tuple[str, str]] = []
    for code, row in candidate_by_code.items():
        lat_raw = (row.get("latitude") or "").strip()
        lon_raw = (row.get("longitude") or "").strip()
        coord_status = (row.get("coordinate_status") or "").strip() or "NOT_VERIFIED"

        # Prefer coordinates present in the main source file; use the explicitly
        # labeled demo overlay only when enabled and source coordinates are blank.
        if bool(lat_raw) != bool(lon_raw):
            raise ValueError(f"Only one of latitude/longitude is present for {code}")
        if not lat_raw and allow_demo_coordinates:
            overlay = coordinate_by_code.get(code)
            if overlay:
                lat_raw = (overlay.get("latitude") or "").strip()
                lon_raw = (overlay.get("longitude") or "").strip()
                coord_status = (overlay.get("coordinate_status") or "DEMO_APPROXIMATE_NOT_VERIFIED").strip()
        if not lat_raw or not lon_raw:
            skipped.append((code, "no coordinates in source; use --allow-demo-coordinates for demo-only overlay"))
            continue

        lat = parse_coordinate(lat_raw, "latitude", code)
        lon = parse_coordinate(lon_raw, "longitude", code)
        planned_pois.append(
            PlannedPOI(
                candidate_code=code,
                poi_id=deterministic_poi_id(code),
                latitude=lat,
                longitude=lon,
                coordinate_status=coord_status,
                is_active=bool(activate_demo_pois),
            )
        )

    included_codes = {poi.candidate_code for poi in planned_pois}
    planned_localizations: list[dict[str, Any]] = []
    for (code, lang), row in localization_by_key.items():
        if code not in included_codes:
            continue
        planned_localizations.append({
            "poi_id": deterministic_poi_id(code),
            "language_code": lang,
            "title": row["title"].strip(),
            "description": row["description"].strip(),
        })

    if not planned_pois:
        raise ValueError(
            "No POI has usable coordinates. Run with --allow-demo-coordinates "
            "to use the clearly labeled demo-only coordinate overlay."
        )

    return ImportPlan(
        pois=planned_pois,
        localizations=planned_localizations,
        skipped_candidates=skipped,
        all_candidate_codes=list(candidate_by_code),
        languages=language_set,
    )


def print_plan(plan: ImportPlan, database: str, apply: bool) -> None:
    print("TCV MongoDB dataset seed plan")
    print(f"Target database: {database}")
    print(f"POI collection: poi ({len(plan.pois)} planned)")
    print(f"Localization collection: poi_localizations ({len(plan.localizations)} planned)")
    print(f"Languages included: {', '.join(sorted(plan.languages))}")
    print(f"POIs set active by this run: {sum(p.is_active for p in plan.pois)}")
    print("Coordinate statuses:")
    for status, count in sorted(Counter(p.coordinate_status for p in plan.pois).items()):
        print(f"  - {status}: {count}")
    print(f"Skipped candidates: {len(plan.skipped_candidates)}")
    for code, reason in plan.skipped_candidates:
        print(f"  - {code}: {reason}")
    if any(p.coordinate_status == "DEMO_APPROXIMATE_NOT_VERIFIED" for p in plan.pois):
        print("WARNING: some coordinates are illustrative demo placements, not verified enclosure coordinates.")
        print("         Do not treat these points as surveyed locations or use them for geofencing.")
    print("Write mode: APPLY" if apply else "Write mode: DRY RUN (no database connection or writes)")


def apply_plan(plan: ImportPlan, mongo_uri: str, database_name: str) -> tuple[int, int]:
    try:
        from bson import ObjectId
        from pymongo import MongoClient, UpdateOne
    except ImportError as error:
        raise RuntimeError("PyMongo is required for --apply. Install the repository backend requirements first.") from error

    if not is_dev_database(database_name):
        raise ValueError(
            "Refusing to write outside a dev/test database. Database name must end in "
            "_dev, _test, -dev, or -test."
        )

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000, appname="tcv-dataset-seed")
    try:
        client.admin.command("ping")
        database = client[database_name]
        poi_collection = database["poi"]
        localization_collection = database["poi_localizations"]

        # Refuse ambiguous duplicate localization keys instead of hiding or deleting them.
        for localization in plan.localizations:
            key_filter = {
                "poi_id": ObjectId(localization["poi_id"]),
                "language_code": localization["language_code"],
            }
            if localization_collection.count_documents(key_filter, limit=2) > 1:
                raise RuntimeError(
                    "Duplicate (poi_id, language_code) exists in target dev DB; "
                    "no import was started. Inspect duplicate rows first."
                )

        poi_ops = []
        for poi in plan.pois:
            set_fields: dict[str, Any] = {
                "latitude": poi.latitude,
                "longitude": poi.longitude,
            }
            update_doc: dict[str, Any] = {"$set": set_fields}
            if poi.is_active:
                set_fields["is_active"] = True
            else:
                update_doc["$setOnInsert"] = {"is_active": False}
            poi_ops.append(UpdateOne({"_id": ObjectId(poi.poi_id)}, update_doc, upsert=True))

        localization_ops = []
        for localization in plan.localizations:
            localization_ops.append(UpdateOne(
                {
                    "poi_id": ObjectId(localization["poi_id"]),
                    "language_code": localization["language_code"],
                },
                {
                    "$set": {
                        "title": localization["title"],
                        "description": localization["description"],
                    },
                    "$setOnInsert": {
                        "poi_id": ObjectId(localization["poi_id"]),
                        "language_code": localization["language_code"],
                    },
                },
                upsert=True,
            ))

        poi_result = poi_collection.bulk_write(poi_ops, ordered=True)
        localization_result = localization_collection.bulk_write(localization_ops, ordered=True)
        poi_touched = poi_result.upserted_count + poi_result.modified_count
        localization_touched = localization_result.upserted_count + localization_result.modified_count
        return poi_touched, localization_touched
    finally:
        client.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR,
                        help=f"Folder with dataset CSV files (default: {DEFAULT_DATA_DIR})")
    parser.add_argument("--mongo-uri", default=os.getenv("MONGODB_URI", DEFAULT_MONGO_URI),
                        help="MongoDB URI. Can also be set using MONGODB_URI.")
    parser.add_argument("--database", default=DEFAULT_DATABASE,
                        help=f"Isolated dev database only (default: {DEFAULT_DATABASE})")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write to MongoDB. Without this, runs a dry-run only.")
    parser.add_argument("--allow-demo-coordinates", action="store_true",
                        help="Use illustrative demo pins for candidates missing mapped coordinates.")
    parser.add_argument("--activate-demo-pois", action="store_true",
                        help="Set imported POIs is_active=true; dev demo only; requires two explicit allow flags.")
    parser.add_argument("--allow-draft-content", action="store_true",
                        help="Acknowledge that translation/narration is still draft content.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not is_dev_database(args.database):
        parser.error("Refusing non-dev database name; use a database ending in _dev, _test, -dev, or -test.")
    if args.activate_demo_pois and not args.apply:
        parser.error("--activate-demo-pois only makes sense with --apply.")

    try:
        plan = build_import_plan(
            args.data_dir,
            allow_demo_coordinates=args.allow_demo_coordinates,
            activate_demo_pois=args.activate_demo_pois,
            allow_draft_content=args.allow_draft_content,
        )
        print_plan(plan, args.database, args.apply)
        if not args.apply:
            print("\nDry-run complete. No MongoDB connection was opened.")
            print("If the plan is correct, rerun with --apply to write to the dev database.")
            if plan.skipped_candidates:
                print("To include missing-coordinate candidates for a class demo, add --allow-demo-coordinates.")
            return 0
        if not args.mongo_uri:
            raise ValueError("MongoDB URI is missing. Set MONGODB_URI or pass --mongo-uri.")
        if args.activate_demo_pois:
            print("WARNING: activating unreviewed demo POIs. Use only in a dedicated dev database.")
        poi_count, localization_count = apply_plan(plan, args.mongo_uri, args.database)
        print(f"\nMongoDB seed finished. POI docs inserted/modified: {poi_count}; localization docs inserted/modified: {localization_count}.")
        print("No records were deleted. Existing localization fields such as audio_url are preserved.")
        return 0
    except Exception as error:
        print(f"ERROR: {error.__class__.__name__}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
