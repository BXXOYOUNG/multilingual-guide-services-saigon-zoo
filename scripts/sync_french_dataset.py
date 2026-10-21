#!/usr/bin/env python3
"""Sync French (fr) localization records from an isolated MongoDB dev DB into dataset CSVs.

Default behavior is a read-only dry run. With --apply, it backs up and updates the source
CSV, language manifest, translation checklist, source register, seeder language rules,
the corresponding seed tests, and existing dataset notes where present.
It never writes to MongoDB, deletes database records, or changes frontend code.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "dataset"
DEFAULT_DATABASE = "saigon_zoo_tcv_dataset_dev"
DEFAULT_MONGO_URI = "mongodb://127.0.0.1:27018/?replicaSet=rs0"
LANGUAGE_ORDER = ["vi", "en", "fr", "zh-Hans", "ja", "ko"]


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.is_file():
        raise ValueError(f"Required file not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {path}")
        return list(reader), list(reader.fieldnames)


def deterministic_poi_id(candidate_code: str) -> str:
    digest = hashlib.sha256(f"tcv-seed-v1:{candidate_code}".encode("utf-8")).hexdigest()
    return digest[:24]


def is_dev_database(database: str) -> bool:
    return database.lower().endswith(("_dev", "_test", "-dev", "-test"))


def map_candidates(candidates: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in candidates:
        code = (row.get("candidate_code") or "").strip()
        if not code:
            raise ValueError("poi_candidates.csv contains an empty candidate_code")
        if code in result:
            raise ValueError(f"Duplicate candidate_code in poi_candidates.csv: {code}")
        result[code] = row
    if not result:
        raise ValueError("poi_candidates.csv contains no rows")
    return result


def build_french_rows(
    candidates: dict[str, dict[str, str]],
    french_docs: list[dict[str, Any]],
    *,
    sync_date: str,
    database_name: str,
) -> list[dict[str, str]]:
    by_id = {deterministic_poi_id(code): code for code in candidates}
    doc_by_code: dict[str, dict[str, Any]] = {}
    unknown_ids: list[str] = []

    for doc in french_docs:
        if (doc.get("language_code") or "").strip() != "fr":
            raise ValueError("MongoDB query returned a document whose language_code is not 'fr'")
        raw_id = doc.get("poi_id")
        if raw_id is None:
            raise ValueError("A French localization document has no poi_id")
        key = str(raw_id).lower()
        code = by_id.get(key)
        if code is None:
            unknown_ids.append(key)
            continue
        if code in doc_by_code:
            raise ValueError(f"Duplicate French MongoDB localization for {code}")
        title = str(doc.get("title") or "").strip()
        description = str(doc.get("description") or "").strip()
        if not title or not description:
            raise ValueError(f"French localization {code} has an empty title or description")
        doc_by_code[code] = doc

    if unknown_ids:
        raise ValueError(
            "French documents reference POI IDs that do not match this dataset's deterministic IDs: "
            + ", ".join(unknown_ids[:5])
        )

    missing = sorted(set(candidates) - set(doc_by_code))
    if missing:
        raise ValueError(
            f"Expected one French localization for every candidate; missing: {', '.join(missing)}"
        )

    rows: list[dict[str, str]] = []
    for code, candidate in candidates.items():
        doc = doc_by_code[code]
        source_url = (candidate.get("species_source_url") or "").strip()
        audio_url = str(doc.get("audio_url") or "").strip()
        audio_status = "AUDIO_URL_PRESENT_IN_DEV_DB_REVIEW_REQUIRED" if audio_url else "NOT_VERIFIED_IN_SOURCE_CSV"
        notes = (
            f"Title/description copied from MongoDB database '{database_name}', collection "
            "'poi_localizations', language_code='fr' during source sync. The database does not "
            "record translator/reviewer provenance in this export; French wording, common names, "
            "facts and pronunciation must be reviewed before audio publication. "
            + ("An audio_url exists in MongoDB but is not copied into this CSV; preserve/review it separately." if audio_url else "The CSV sync does not claim that French audio exists.")
        )
        rows.append({
            "candidate_code": code,
            "language_code": "fr",
            "title": str(doc["title"]).strip(),
            "description": str(doc["description"]).strip(),
            "content_status": "DATABASE_EXPORTED_DRAFT_REVIEW_REQUIRED",
            "fact_review_status": "PENDING_SOURCE_FACT_REVIEW",
            "translation_review_status": "FRENCH_EDITOR_REVIEW_REQUIRED",
            "title_review_note": "Title copied from the local development database; independent French common-name/editorial review has not been documented.",
            "source_url": source_url,
            # Leave blank: syncing data is not a source fact-check.
            "source_checked_date": "",
            "audio_status": audio_status,
            "review_notes": notes,
        })
    return rows


def ordered_localization_rows(
    existing_rows: list[dict[str, str]],
    french_rows: list[dict[str, str]],
    candidate_order: list[str],
    fields: list[str],
) -> list[dict[str, str]]:
    combined = [r for r in existing_rows if (r.get("language_code") or "").strip() != "fr"] + french_rows
    candidate_index = {code: i for i, code in enumerate(candidate_order)}
    language_index = {code: i for i, code in enumerate(LANGUAGE_ORDER)}
    combined.sort(key=lambda r: (
        candidate_index.get((r.get("candidate_code") or "").strip(), 9999),
        language_index.get((r.get("language_code") or "").strip(), 9999),
    ))
    return [{field: str(row.get(field) or "") for field in fields} for row in combined]


def merge_keyed_rows(
    existing_rows: list[dict[str, str]],
    new_rows: list[dict[str, str]],
    fields: list[str],
    key_fields: tuple[str, str],
    candidate_order: list[str],
) -> list[dict[str, str]]:
    merged: dict[tuple[str, str], dict[str, str]] = {}
    for row in existing_rows:
        key = ((row.get(key_fields[0]) or "").strip(), (row.get(key_fields[1]) or "").strip())
        if key[0] and key[1] and key[1] != "fr":
            if key in merged:
                raise ValueError(f"Duplicate existing review/checklist row: {key}")
            merged[key] = row
    for row in new_rows:
        key = ((row.get(key_fields[0]) or "").strip(), (row.get(key_fields[1]) or "").strip())
        merged[key] = row
    candidate_index = {code: i for i, code in enumerate(candidate_order)}
    language_index = {code: i for i, code in enumerate(LANGUAGE_ORDER)}
    result = list(merged.values())
    result.sort(key=lambda r: (
        candidate_index.get((r.get(key_fields[0]) or "").strip(), 9999),
        language_index.get((r.get(key_fields[1]) or "").strip(), 9999),
    ))
    return [{field: str(row.get(field) or "") for field in fields} for row in result]


def build_checklist_rows(french_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    result = []
    for row in french_rows:
        result.append({
            "candidate_code": row["candidate_code"],
            "language_code": "fr",
            "title": row["title"],
            "title_review_required": "YES",
            "native_language_review": "NO",
            "terminology_review": "PENDING",
            "fact_alignment_review": "PENDING_REVIEW",
            "tts_pronunciation_review": "PENDING_AUDIO_PHASE",
            "approved_for_audio": "NO",
            "review_notes": row["review_notes"],
        })
    return result


def build_manifest_row() -> dict[str, str]:
    return {
        "language_code": "fr",
        "language_name": "French",
        "native_name": "Français",
        "script": "Latin",
        "standard": "ISO 639-1",
        "status": "Database localization imported; editorial and French terminology review required",
        "runtime_integration_note": "Local API verification on 2026-10-20: GET /api/pois?language=fr returned 11 POIs. Browser selector flow should still be checked.",
        "localization_records": "11",
        "human_review_complete": "No",
    }


def merge_manifest(existing_rows: list[dict[str, str]], fields: list[str]) -> list[dict[str, str]]:
    by_code: dict[str, dict[str, str]] = {}
    for row in existing_rows:
        code = (row.get("language_code") or "").strip()
        if not code:
            continue
        if code in by_code:
            raise ValueError(f"Duplicate language code in language_manifest.csv: {code}")
        by_code[code] = row
    by_code["fr"] = build_manifest_row()
    return [{field: str(by_code[code].get(field) or "") for field in fields} for code in LANGUAGE_ORDER if code in by_code]


def merge_source_register(existing_rows: list[dict[str, str]], fields: list[str], sync_date: str, db_name: str) -> list[dict[str, str]]:
    rows = [r for r in existing_rows if (r.get("source_id") or "").strip() != "SRC-MONGO-FR-001"]
    record = {
        "source_id": "SRC-MONGO-FR-001",
        "candidate_code": "ALL",
        "publisher": "Project local MongoDB development database",
        "source_title": "French localization export (language_code=fr)",
        "url": "",
        "fields_used": "Copied title/description values from poi_localizations where language_code=fr; this is a data-provenance record, not an independent fact or translation verification.",
        "checked_date": sync_date,
        "limits_or_notes": f"Exported from database '{db_name}'. Translator/reviewer provenance is not embedded in these records; French common names, grammar, zoological facts and audio suitability remain pending review.",
    }
    rows.append(record)
    return [{field: str(row.get(field) or "") for field in fields} for row in rows]


def patch_seed_script(text: str) -> str:
    pattern = r'^REQUIRED_LANGUAGES\s*=\s*\{[^\n]*\}$'
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        raise ValueError("Could not find REQUIRED_LANGUAGES constant in scripts/seed_dataset.py")
    replacement = 'REQUIRED_LANGUAGES = {"vi", "en", "fr", "zh-Hans", "ja", "ko"}'
    if match.group(0) == replacement:
        return text
    return text[:match.start()] + replacement + text[match.end():]


def patch_seed_tests(text: str) -> str:
    text2 = text.replace("assert len(plan.localizations) == 10", "assert len(plan.localizations) == 12")
    text2 = text2.replace("assert len(plan.localizations) == 55", "assert len(plan.localizations) == 66")
    text2 = text2.replace('"vi", "en", "zh-Hans", "ja", "ko"', '"vi", "en", "fr", "zh-Hans", "ja", "ko"')
    if text2 == text and ("== 12" not in text or "== 66" not in text or '"fr"' not in text):
        raise ValueError("Could not apply the expected six-language updates to tests/test_seed_dataset.py")
    return text2


def patch_seed_readme(text: str) -> str:
    replacements = [
        ("up to 55 localization documents", "up to 66 localization documents"),
        ("10 localization rows", "12 localization rows"),
        ("55 localization rows", "66 localization rows"),
        ("55 localization documents", "66 localization documents"),
        ("55 localization", "66 localization"),
        ("55 localization rows;", "66 localization rows;"),
        ("`vi`, `en`, `zh-Hans`, `ja`, `ko`", "`vi`, `en`, `fr`, `zh-Hans`, `ja`, `ko`"),
        ("zh-Hans`, `ja`, and `ko`", "zh-Hans`, `ja`, `ko`, and `fr`"),
    ]
    result = text
    for old, new in replacements:
        result = result.replace(old, new)
    return result


def patch_phase3a_readme(text: str) -> str:
    result = text
    result = result.replace("for 5 ngôn ngữ: `vi`, `en`, `zh-Hans`, `ja`, `ko`", "for 6 ngôn ngữ: `vi`, `en`, `fr`, `zh-Hans`, `ja`, `ko`")
    result = result.replace("đủ 5 ngôn ngữ", "đủ 6 ngôn ngữ")
    result = result.replace("55 bản ghi (11 POI × 5 ngôn ngữ)", "66 bản ghi (11 POI × 6 ngôn ngữ)")
    result = result.replace("Bản dịch do AI biên soạn cần người thông thạo từng ngôn ngữ", "Bản dịch do AI biên soạn và nội dung tiếng Pháp đồng bộ từ database cần người thông thạo từng ngôn ngữ")
    return result


def patch_app_notes(text: str) -> str:
    result = text.replace("The dataset has five language codes: `vi`, `en`, `zh-Hans`, `ja`, and `ko`.", "The dataset has six language codes: `vi`, `en`, `fr`, `zh-Hans`, `ja`, and `ko`.")
    result = result.replace("update the frontend language selector/context to emit the exact same code and test `GET /api/pois?language=<code>` for each locale.", "the frontend selector currently declares all six language options; verify the browser selection flow and exact `GET /api/pois?language=<code>` request for each locale.")
    result = result.replace("Add the three extra language options to the UI (if they are not already supported).", "The six language options are declared in the UI; confirm browser end-to-end language switching.")
    result = result.replace("Add API tests confirming exact-match localization for each language.", "Local development API checks on 2026-10-20 returned 11 POIs for vi, en, fr, zh-Hans, ja, and ko; keep regression tests for exact-match localization.")
    result = result.replace("five language", "six language").replace("five languages", "six languages")
    return result


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def backup_and_write(path: Path, content: str, backup_stamp: str) -> None:
    if path.exists():
        backup_path = path.with_name(f"{path.name}.bak-{backup_stamp}")
        if not backup_path.exists():
            shutil.copy2(path, backup_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8-sig", newline="")
    tmp.replace(path)


def csv_content(rows: list[dict[str, str]], fields: list[str]) -> str:
    from io import StringIO
    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--mongo-uri", default=os.getenv("MONGODB_URI", DEFAULT_MONGO_URI))
    parser.add_argument("--database", default=os.getenv("MONGODB_DATABASE", DEFAULT_DATABASE))
    parser.add_argument("--apply", action="store_true", help="Write updated CSV/source files; without this, dry-run only")
    args = parser.parse_args(argv)

    if not is_dev_database(args.database):
        parser.error("Refusing to read source localization from a non-dev/test DB; use a DB name ending in _dev, _test, -dev, or -test.")

    try:
        data_dir = args.data_dir.resolve()
        candidates_rows, _ = read_csv(data_dir / "poi_candidates.csv")
        candidates = map_candidates(candidates_rows)
        loc_path = data_dir / "poi_localizations_multilingual_v2.csv"
        loc_rows, loc_fields = read_csv(loc_path)
        manifest_path = data_dir / "language_manifest.csv"
        manifest_rows, manifest_fields = read_csv(manifest_path)
        checklist_path = data_dir / "translation_review_checklist.csv"
        checklist_rows, checklist_fields = read_csv(checklist_path)
        source_path = data_dir / "source_register.csv"
        source_rows, source_fields = read_csv(source_path)

        from pymongo import MongoClient

        client = MongoClient(args.mongo_uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
        try:
            client.admin.command("ping")
            french_docs = list(client[args.database]["poi_localizations"].find({"language_code": "fr"}))
        finally:
            client.close()

        today = date.today().isoformat()
        french_rows = build_french_rows(candidates, french_docs, sync_date=today, database_name=args.database)
        updated_localizations = ordered_localization_rows(loc_rows, french_rows, list(candidates), loc_fields)
        updated_checklist = merge_keyed_rows(checklist_rows, build_checklist_rows(french_rows), checklist_fields, ("candidate_code", "language_code"), list(candidates))
        updated_manifest = merge_manifest(manifest_rows, manifest_fields)
        updated_sources = merge_source_register(source_rows, source_fields, today, args.database)

        # Check the final source matrix is exactly one row per POI/language.
        counts: dict[str, int] = {}
        pairs: set[tuple[str, str]] = set()
        for row in updated_localizations:
            key = (row["candidate_code"], row["language_code"])
            if key in pairs:
                raise ValueError(f"Duplicate final localization row: {key}")
            pairs.add(key)
            counts[row["language_code"]] = counts.get(row["language_code"], 0) + 1
        expected_pairs = len(candidates) * len(LANGUAGE_ORDER)
        if len(updated_localizations) != expected_pairs:
            raise ValueError(f"Expected {expected_pairs} localization rows after sync, got {len(updated_localizations)}")
        for language in LANGUAGE_ORDER:
            if counts.get(language) != len(candidates):
                raise ValueError(f"Expected {len(candidates)} rows for {language}, got {counts.get(language, 0)}")

        seed_path = ROOT / "scripts" / "seed_dataset.py"
        tests_path = ROOT / "tests" / "test_seed_dataset.py"
        if not seed_path.exists():
            raise ValueError(f"Seeder not found: {seed_path}")
        if not tests_path.exists():
            raise ValueError(f"Seeder tests not found: {tests_path}")
        updated_seed = patch_seed_script(read_text(seed_path))
        updated_tests = patch_seed_tests(read_text(tests_path))

        file_updates: dict[Path, str] = {
            loc_path: csv_content(updated_localizations, loc_fields),
            manifest_path: csv_content(updated_manifest, manifest_fields),
            checklist_path: csv_content(updated_checklist, checklist_fields),
            source_path: csv_content(updated_sources, source_fields),
            seed_path: updated_seed,
            tests_path: updated_tests,
        }
        # If the older compatibility filename exists, keep it in sync so it does not
        # silently remain a stale 5-language copy.
        legacy_loc_path = data_dir / "poi_localizations_multilingual_draft.csv"
        if legacy_loc_path.exists():
            _, legacy_fields = read_csv(legacy_loc_path)
            needed_fields = set(loc_fields)
            if not needed_fields.issubset(set(legacy_fields)):
                raise ValueError(
                    "Legacy localization CSV has a different schema; refusing to overwrite it: "
                    f"{legacy_loc_path}"
                )
            file_updates[legacy_loc_path] = csv_content(updated_localizations, legacy_fields)
        optional_patches = [
            (ROOT / "README_SEED_DATASET.md", patch_seed_readme),
            (data_dir / "README_PHASE3A_CONTENT_QA.md", patch_phase3a_readme),
            (data_dir / "APPLICATION_INTEGRATION_NOTES.md", patch_app_notes),
        ]
        for path, patcher in optional_patches:
            if path.exists():
                file_updates[path] = patcher(read_text(path))

        print("French localization source-sync plan")
        print(f"Source database: {args.database} (read-only; no DB writes)")
        print(f"POI candidates: {len(candidates)}")
        print(f"French records read from MongoDB: {len(french_docs)}")
        print(f"Localization source CSV: {len(updated_localizations)} rows")
        print("Languages: " + ", ".join(f"{lang}={counts.get(lang, 0)}" for lang in LANGUAGE_ORDER))
        print(f"Checklist rows: {len(updated_checklist)}")
        print(f"Manifest languages: {len(updated_manifest)}")
        print(f"Files to update: {len(file_updates)}")
        print("French review status: REQUIRED; approved_for_audio=NO")
        print("MongoDB will not be modified by this script.")

        if not args.apply:
            print("Mode: DRY RUN (no files changed)")
            print("If this plan is correct, rerun with --apply.")
            return 0

        backup_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        for path, content in file_updates.items():
            backup_and_write(path, content, backup_stamp)
            print(f"Updated: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
        print("\nFrench localization sync complete. CSV source now contains 66 rows (11 POIs × 6 languages).")
        print("Backups were created next to each updated file using .bak-<timestamp> suffixes.")
        print("Next: python -m pytest -q tests/test_seed_dataset.py && python scripts/seed_dataset.py --allow-demo-coordinates")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
