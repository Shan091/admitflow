"""Public reference imports reject untrusted source URLs and ambiguous duplicate names."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.scripts.replace_demo_catalogue import PublicCatalogue


def dataset():
    return json.loads(
        (Path(__file__).parents[1] / "data/jain-kochi/catalogue.json").read_text(encoding="utf-8")
    )


def test_real_snapshot_has_verified_campus_sources_without_seats_or_fees():
    catalog = PublicCatalogue.model_validate(dataset())
    assert len(catalog.programmes) == 64
    assert all("/kochi/" in p.source_url for p in catalog.programmes)


@pytest.mark.parametrize(
    "url", ["http://127.0.0.1/admin", "https://other.example/kochi/course", "javascript:alert(1)"]
)
def test_import_rejects_nonofficial_reference_sources(url):
    raw = dataset()
    raw["programmes"][0]["source_url"] = url
    with pytest.raises(ValidationError):
        PublicCatalogue.model_validate(raw)


def test_import_requires_unambiguous_programme_names():
    raw = dataset()
    raw["programmes"][1]["name"] = raw["programmes"][0]["name"]
    with pytest.raises(ValidationError):
        PublicCatalogue.model_validate(raw)
