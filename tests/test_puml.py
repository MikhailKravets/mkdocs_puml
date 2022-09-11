from src import PlantUML
from tests.conftest import BASE_PUML_URL


def test_translate(diagram_and_encoded: (str, str), svg_diagram: str, mock_requests):
    _, encoded = diagram_and_encoded

    puml = PlantUML(BASE_PUML_URL)
    resp = puml.translate(encoded)

    assert resp.startswith(f'<div class="{puml.div_class}">')
    assert not puml._html_comment_regex.search(resp)
    assert 'preserveAspectRatio="true"' in resp
