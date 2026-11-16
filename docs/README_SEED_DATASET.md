# TCV MongoDB seed kit (student-project dataset)

This kit prepares the Phase 3A multilingual CSV drafts for the project's existing MongoDB collections. It does not connect to the database unless `--apply` is supplied.

> Maintenance tool, not the default startup or handoff workflow. The classroom demo has 11 active simulated POIs and 6 offline packages. Do not rerun seed over edited content without backing up and checking whether existing audio still matches the text. See `docs/CURRENT_ARCHITECTURE.md`.

## Important behavior

- Default mode is **dry-run**: validates CSV files and prints the import plan; no database connection and no writes.
- Writes only to a dev/test database name ending in `_dev`, `_test`, `-dev`, or `-test`. Default: `saigon_zoo_tcv_dataset_dev`.
- Uses current backend collections and fields:
  - `poi`: `_id`, `latitude`, `longitude`, `is_active`
  - `poi_localizations`: `poi_id`, `language_code`, `title`, `description`
- Uses deterministic BSON ObjectIds derived from `candidate_code`, so repeated imports use the same `poi_id` links.
- Does not delete records or drop databases. Upserts only the selected POI/localization rows.
- Localization updates change only `title` and `description`; existing fields such as `audio_url` are preserved.
- POIs are inactive on first insert by default. Existing `is_active` values are not turned off by a normal rerun.
- Two points (elephant and giraffe) use public OpenStreetMap node coordinates that have not been field-verified. The remaining nine coordinates are explicitly **illustrative demo coordinates**, not real verified enclosure locations.
- Activating unreviewed POIs requires all three flags: `--apply --allow-demo-coordinates --activate-demo-pois --allow-draft-content`. Use only against a dev database. Do not use the demo coordinates for geofencing or claim they are field-verified.
- Dataset text is draft copy/translation. Human review is still needed before treating narration/audio as official.

## 1. Place files in the repository

Extract/merge this kit into the repo root so these paths exist:

```text
scripts/seed_dataset.py
data/dataset/poi_candidates.csv
data/dataset/poi_localizations_multilingual_v2.csv
data/dataset/poi_demo_coordinates.csv
data/dataset/language_manifest.csv
data/dataset/source_register.csv
data/dataset/content_fact_review.csv
data/dataset/translation_review_checklist.csv
data/dataset/coordinate_verification_template.csv
tests/test_seed_dataset.py
```

Other source/reference CSVs are included for provenance. The script itself imports only the `poi_candidates.csv`, `poi_localizations_multilingual_v2.csv`, `language_manifest.csv`, and `poi_demo_coordinates.csv` files.

## 2. Run local tests

From the repository root, using the project's `.venv`:

```powershell
python -m pytest -q tests/test_seed_dataset.py
```

These tests do not connect to MongoDB.

## 3. Dry-run using only coordinates already present in the main candidate CSV

```powershell
python scripts/seed_dataset.py
```

At present this should plan 2 POIs and 12 localization rows, and skip the 9 candidates that lack coordinates in the primary CSV. No database connection is opened.

## 4. Dry-run with demo-only coordinate overlay (recommended for a student demo)

```powershell
python scripts/seed_dataset.py --allow-demo-coordinates
```

This should plan 11 POIs and 66 localization rows while keeping every POI inactive. Inspect the report and the `poi_demo_coordinates.csv` status fields before writing.

## 5. Seed into a dedicated local dev database

Set the local URI (adapt the port/replica-set option if your MongoDB container differs):

```powershell
$env:MONGODB_URI = "mongodb://127.0.0.1:27018/?replicaSet=rs0"
python scripts/seed_dataset.py --allow-demo-coordinates --apply
```

This writes to `saigon_zoo_tcv_dataset_dev`, not the application's configured database. It inserts/updates the 11 POIs as inactive and creates/upserts up to 66 localization documents. It does not connect to or mutate another database name.

## 6. Optional: activate demo points so GET /api/pois can return them

The current POI API filters on `poi.is_active == true`. If you explicitly want to display approximate points and draft copy in a class demo, run:

```powershell
python scripts/seed_dataset.py --allow-demo-coordinates --allow-draft-content --activate-demo-pois --apply
```

This still targets the dedicated database `saigon_zoo_tcv_dataset_dev`. Configure the running API to use that same DB before testing. These coordinates are unsuitable for geofencing and must be described in the report as illustrative demo positions.

## 7. Verify documents with mongosh

```javascript
use saigon_zoo_tcv_dataset_dev
db.poi.countDocuments({})
db.poi.countDocuments({ is_active: true })
db.poi_localizations.countDocuments({})
db.poi_localizations.countDocuments({ language_code: "zh-Hans" })
db.poi.findOne({}, { latitude: 1, longitude: 1, is_active: 1 })
db.poi_localizations.findOne({}, { poi_id: 1, language_code: 1, title: 1, description: 1 })
```

On a clean dev database, expected with demo coordinates loaded: 11 POIs; 0 active after the normal seed, or 11 active after the explicit activation command; 66 localization rows; 11 rows per language. If rerun, counts should not increase. A normal rerun intentionally preserves existing `is_active` values rather than deactivating records that were explicitly activated earlier.

## Notes

- The API repository currently queries collection `poi` for active records, then matches `poi_localizations` by BSON `poi_id` and exact `language_code`. This kit matches those fields.
- The script does not modify the frontend language selector. `zh-Hans`, `ja`, `ko`, and `fr` must be supported by the UI and passed exactly to `GET /api/pois?language=...` to display translations.
- Do not configure the running application to use the seeded database until you intentionally choose to test this dataset.
