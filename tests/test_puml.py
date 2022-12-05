import pytest

from mkdocs_puml.puml import PlantUML
from tests.conftest import BASE_PUML_URL


def test_url_with_slash():
    puml = PlantUML(BASE_PUML_URL)
    assert puml.base_url.endswith('/')


def test_url_without_slash():
    puml = PlantUML(BASE_PUML_URL[:-1])
    assert puml.base_url.endswith('/')


def test_num_worker_less_or_equal_zero():
    with pytest.raises(ValueError):
        PlantUML(BASE_PUML_URL, num_workers=0)


def test_translate(diagram_and_encoded: (str, str), mock_requests):
    diagram, encoded = diagram_and_encoded

    diagrams = [diagram] * 2

    puml = PlantUML(BASE_PUML_URL)
    resp = puml.translate(diagrams)

    assert puml.base_url.endswith('/')

    assert len(resp) == 2

    for r in resp:
        assert r.startswith("<svg")
        assert not puml._html_comment_regex.search(r)
        assert 'preserveAspectRatio="true"' in r
