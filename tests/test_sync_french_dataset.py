from pathlib import Path
import importlib.util

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sync_french_dataset.py"
spec = importlib.util.spec_from_file_location("sync_french_dataset", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_deterministic_id_matches_seed_script_algorithm():
    import hashlib
    expected = hashlib.sha256(b"tcv-seed-v1:TCV-AN-001").hexdigest()[:24]
    assert module.deterministic_poi_id("TCV-AN-001") == expected


def test_dev_database_guard():
    assert module.is_dev_database("saigon_zoo_tcv_dataset_dev")
    assert module.is_dev_database("tcv_dataset_test")
    assert not module.is_dev_database("saigon_zoo")


def test_build_french_rows_maps_by_candidate_and_marks_review_pending():
    candidates = {
        "TCV-AN-001": {
            "species_source_url": "https://example.test/hippo",
            "name_vi": "Hà mã",
        }
    }
    poi_id = module.deterministic_poi_id("TCV-AN-001")
    rows = module.build_french_rows(
        candidates,
        [{
            "poi_id": poi_id,
            "language_code": "fr",
            "title": "Hippopotame",
            "description": "Texte de démonstration à réviser.",
        }],
        sync_date="2026-10-20",
        database_name="saigon_zoo_tcv_dataset_dev",
    )
    assert len(rows) == 1
    assert rows[0]["candidate_code"] == "TCV-AN-001"
    assert rows[0]["language_code"] == "fr"
    assert rows[0]["approved_for_audio"] if "approved_for_audio" in rows[0] else rows[0]["audio_status"] == "NOT_VERIFIED_IN_SOURCE_CSV"
    assert rows[0]["translation_review_status"] == "FRENCH_EDITOR_REVIEW_REQUIRED"
    assert rows[0]["source_checked_date"] == ""


def test_build_french_rows_rejects_missing_or_unknown_poi():
    candidates = {"TCV-AN-001": {"species_source_url": ""}}
    try:
        module.build_french_rows(
            candidates,
            [{"poi_id": "000000000000000000000000", "language_code": "fr", "title": "X", "description": "Y"}],
            sync_date="2026-10-20",
            database_name="saigon_zoo_tcv_dataset_dev",
        )
    except ValueError as exc:
        assert "do not match" in str(exc)
    else:
        raise AssertionError("Unknown POI ID should be rejected")


def test_seed_script_language_constant_includes_french():
    patched = module.patch_seed_script('REQUIRED_LANGUAGES = {"vi", "en", "zh-Hans", "ja", "ko"}\n')
    assert '"fr"' in patched


def test_seed_test_expectations_are_updated():
    source = '''assert len(plan.localizations) == 10
    assert len(plan.localizations) == 55
    assert {loc["language_code"] for loc in plan.localizations} == {
        "vi", "en", "zh-Hans", "ja", "ko"
    }
'''
    patched = module.patch_seed_tests(source)
    assert "== 12" in patched
    assert "== 66" in patched
    assert '"fr"' in patched
