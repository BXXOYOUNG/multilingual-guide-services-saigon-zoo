from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from seed_dataset import (  # noqa: E402
    build_import_plan,
    deterministic_poi_id,
    is_dev_database,
)

DATA_DIR = ROOT / "data" / "dataset"


def test_default_dry_run_uses_only_source_coordinates():
    plan = build_import_plan(DATA_DIR)
    assert len(plan.pois) == 2
    assert len(plan.localizations) == 12
    assert len(plan.skipped_candidates) == 9
    assert all(not poi.is_active for poi in plan.pois)


def test_demo_coordinates_include_all_candidate_pois():
    plan = build_import_plan(DATA_DIR, allow_demo_coordinates=True)
    assert len(plan.pois) == 11
    assert len(plan.localizations) == 66
    assert len(plan.skipped_candidates) == 0
    assert {loc["language_code"] for loc in plan.localizations} == {
        "vi", "en", "fr", "zh-Hans", "ja", "ko"
    }


def test_all_poi_ids_are_valid_and_deterministic():
    import re
    plan = build_import_plan(DATA_DIR, allow_demo_coordinates=True)
    assert all(re.fullmatch(r"[0-9a-f]{24}", poi.poi_id) for poi in plan.pois)
    assert deterministic_poi_id("TCV-AN-001") == deterministic_poi_id("TCV-AN-001")
    assert deterministic_poi_id("TCV-AN-001") != deterministic_poi_id("TCV-AN-002")


def test_default_seed_keeps_pois_inactive():
    plan = build_import_plan(DATA_DIR, allow_demo_coordinates=True)
    assert all(poi.is_active is False for poi in plan.pois)


def test_activation_requires_demo_coordinates():
    with pytest.raises(ValueError, match="requires --allow-demo-coordinates"):
        build_import_plan(DATA_DIR, activate_demo_pois=True, allow_draft_content=True)


def test_activation_requires_explicit_draft_acknowledgement():
    with pytest.raises(ValueError, match="requires --allow-draft-content"):
        build_import_plan(DATA_DIR, allow_demo_coordinates=True, activate_demo_pois=True)


def test_activation_only_when_both_acknowledgements_present():
    plan = build_import_plan(
        DATA_DIR,
        allow_demo_coordinates=True,
        activate_demo_pois=True,
        allow_draft_content=True,
    )
    assert len(plan.pois) == 11
    assert all(poi.is_active is True for poi in plan.pois)


def test_dev_database_guard():
    assert is_dev_database("saigon_zoo_tcv_dataset_dev")
    assert is_dev_database("tcv_seed_test")
    assert not is_dev_database("saigon_zoo")
    assert not is_dev_database("production")
