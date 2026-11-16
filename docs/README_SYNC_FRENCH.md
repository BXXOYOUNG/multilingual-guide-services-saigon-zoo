# TCV French localization source sync

This helper reads the existing French (`fr`) records from the **local development MongoDB** and makes the CSV dataset/manifest/checklist match that source. It does not write to MongoDB. Default mode is a dry run; `--apply` updates files and creates backups beside each changed file.

> Maintenance tool for synchronizing French source files. Normal startup and transferring an existing demo do not require this sync.

## Files expected in your repository

- `data/dataset/poi_candidates.csv`
- `data/dataset/poi_localizations_multilingual_v2.csv`
- `data/dataset/language_manifest.csv`
- `data/dataset/translation_review_checklist.csv`
- `data/dataset/source_register.csv`
- `scripts/seed_dataset.py`
- `tests/test_seed_dataset.py`

Merge the `scripts/` and `tests/` folders from this kit into the repository root. Do not copy the `data/` folder from this kit; it does not contain the user's actual French strings.

## 1. Check local dev DB and run dry-run

In PowerShell at repo root:

```powershell
$env:MONGODB_URI = "mongodb://127.0.0.1:27018/?replicaSet=rs0"
$env:MONGODB_DATABASE = "saigon_zoo_tcv_dataset_dev"
python scripts/sync_french_dataset.py
```

Expected summary: 11 French records from MongoDB, 66 source localization rows after merging, and 11 per language (`vi`, `en`, `fr`, `zh-Hans`, `ja`, `ko`). The script verifies MongoDB POI IDs match the deterministic IDs derived from `candidate_code`. It aborts rather than guessing if IDs are unknown, records are missing, or titles/descriptions are blank.

## 2. Apply to source files

Only after reviewing the dry-run:

```powershell
python scripts/sync_french_dataset.py --apply
```

The script updates the source localization CSV, language manifest, translation review checklist, source register, seed script's required language set, seed test expectations, and documentation files if those files exist. Before each update it creates a side-by-side `.bak-<timestamp>` backup. It never modifies MongoDB.

French rows are marked as requiring editorial, terminology and fact review; they are not approved for audio. If an `audio_url` is present in MongoDB, the sync records that in a review status but does not export the URL into the source text CSV.

## 3. Verify

```powershell
python -m pytest -q tests/test_sync_french_dataset.py
python -m pytest -q tests/test_seed_dataset.py
python scripts/seed_dataset.py --allow-demo-coordinates
```

The seeder plan should report 2 POIs and 12 localization rows without the demo-coordinate overlay, or 11 POIs and 66 localization rows with `--allow-demo-coordinates`. Do not add `--activate-demo-pois` unless you intentionally need the draft coordinates and draft narration to appear in the local class demo.

## Important

- This tool reads only a development/test database name and is read-only toward MongoDB.
- The current local database is treated as the immediate source for French text because the original translator/source data was not present in the CSV bundle.
- The French translation's external provenance is not known from the database fields; each row therefore remains marked for review and cannot be considered formally approved.
- The script does not create audio and does not change frontend code. The frontend already declares `fr` per the latest inspected source.
