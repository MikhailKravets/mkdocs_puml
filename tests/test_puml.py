from mkdocs_puml import PlantUML
from tests.conftest import BASE_PUML_URL


def test_url_with_slash():
    puml = PlantUML(BASE_PUML_URL)
    assert puml.base_url.endswith('/')


def test_url_without_slash():
    puml = PlantUML(BASE_PUML_URL[:-1])
    assert puml.base_url.endswith('/')


def test_translate(diagram_and_encoded: (str, str), mock_requests):
    _, encoded = diagram_and_encoded

    puml = PlantUML(BASE_PUML_URL)
    resp = puml.translate(encoded)

    assert puml.base_url.endswith('/')
    assert resp.startswith("<svg")
    assert not puml._html_comment_regex.search(resp)
    assert 'preserveAspectRatio="true"' in resp
