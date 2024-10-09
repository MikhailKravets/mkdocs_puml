import pytest

from mkdocs_puml.puml import PlantUML
from tests.conftest import BASE_PUML_URL


def test_num_worker_less_or_equal_zero():
    # Confirm ValueError raised for invalid num_workers
    with pytest.raises(ValueError, match="`num_workers` argument should be bigger than 0."):
        PlantUML(BASE_PUML_URL, num_workers=0)

    with pytest.raises(ValueError, match="`num_workers` argument should be bigger than 0."):
        PlantUML(BASE_PUML_URL, num_workers=-1)


def test_translate(diagram_and_encoded: tuple[str, str], mock_requests):
    # Verify translation of multiple diagrams to SVG
    diagram, encoded = diagram_and_encoded

    diagrams = [diagram] * 2

    puml = PlantUML(BASE_PUML_URL)
    resp = puml.translate(diagrams)

    assert puml.base_url == f"{BASE_PUML_URL}svg"

    assert len(resp) == 2

    for r in resp:
        assert r.startswith("<svg")
        assert not puml._html_comment_regex.search(r)
        assert 'preserveAspectRatio="xMidYMid meet"' in r
