from markdown import Markdown

from src import PlantUML
from src.extensions import makeExtension, PumlExtension, PumlPreprocessor
from tests.conftest import BASE_PUML_URL


def test_make_extension():
    name = "puml"
    url = BASE_PUML_URL

    ext = makeExtension(name=name, puml_url=url)

    assert isinstance(ext, PumlExtension)
    assert ext.name == name
    assert ext.puml.base_url == url


def test_puml_extension():
    name = "puml"
    url = BASE_PUML_URL

    md = Markdown()

    ext = PumlExtension(name, url)
    ext.extendMarkdown(md)

    assert 'puml' in md.preprocessors


def test_puml_preprocessor(md_lines, svg_diagram, mock_requests):
    name = "puml"
    url = BASE_PUML_URL

    puml = PlantUML(url)
    md = Markdown()

    preprocessor = PumlPreprocessor(md, name, puml)

    resp = preprocessor.run(md_lines)
    resp = ''.join(resp)

    assert resp.count(f'<div class="{name}">') == 2
    assert mock_requests.call_count == 2
