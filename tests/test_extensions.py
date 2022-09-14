from markdown import Markdown

from mkdocs_puml import PlantUML
from mkdocs_puml.extensions import makeExtension, PumlExtension, PumlPreprocessor
from tests.conftest import BASE_PUML_URL


def test_make_extension():
    url = BASE_PUML_URL

    ext = makeExtension(puml_url=url)

    assert isinstance(ext, PumlExtension)
    assert ext.puml.base_url == url


def test_puml_extension():
    url = BASE_PUML_URL

    md = Markdown()

    ext = PumlExtension(url)
    ext.extendMarkdown(md)

    assert 'puml' in md.preprocessors


def test_puml_preprocessor(md_lines, svg_diagram, mock_requests):
    url = BASE_PUML_URL

    puml = PlantUML(url)
    md = Markdown()

    preprocessor = PumlPreprocessor(md, puml)

    resp = preprocessor.run(md_lines)
    resp = ''.join(resp)

    assert resp.count('<div class="puml">') == 2
    assert mock_requests.call_count == 2
