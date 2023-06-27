import uuid
from unittest.mock import MagicMock

import jinja2
import pytest

from uuid import UUID

from mkdocs.config.config_options import Config

from mkdocs_puml.plugin import PlantUMLPlugin
from tests.conftest import BASE_PUML_URL, CUSTOM_PUML_KEYWORD, TESTDATA_DIR


def is_uuid_valid(uuid_str: str) -> bool:
    """Check whether uuid_str is valid uuid4

    Args:
        uuid_str: uuid to test

    Returns:
        Boolean designating if uuid_str is valid
    """
    try:
        uuid_obj = UUID(uuid_str, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_str


@pytest.fixture
def plugin_config():
    c = Config(schema=PlantUMLPlugin.config_scheme)
    c['puml_url'] = BASE_PUML_URL
    return c


@pytest.fixture
def plugin_config_custom_keyword():
    c = Config(schema=PlantUMLPlugin.config_scheme)
    c['puml_url'] = BASE_PUML_URL
    c['puml_keyword'] = CUSTOM_PUML_KEYWORD
    return c


@pytest.fixture
def plugin_environment():
    loader = jinja2.FileSystemLoader(searchpath=TESTDATA_DIR)
    return jinja2.Environment(loader=loader)


@pytest.fixture
def plant_uml_plugin(plugin_config):
    plugin = PlantUMLPlugin()
    c = Config(schema=plugin.config_scheme)
    c['puml_url'] = BASE_PUML_URL
    plugin.config = c
    plugin.on_config(c)

    return plugin


@pytest.fixture
def plant_uml_plugin_custom_keyword(plugin_config_custom_keyword):
    plugin = PlantUMLPlugin()
    c = Config(schema=plugin.config_scheme)
    c['puml_url'] = BASE_PUML_URL
    c['puml_keyword'] = CUSTOM_PUML_KEYWORD
    plugin.config = c
    plugin.on_config(c)

    return plugin


@pytest.fixture
def diagrams_dict(diagram_and_encoded):
    return {
        str(uuid.uuid4()): diagram_and_encoded[0],
        str(uuid.uuid4()): diagram_and_encoded[0],
        str(uuid.uuid4()): diagram_and_encoded[0],
    }


@pytest.fixture(scope="package")
def md_lines():
    with open(TESTDATA_DIR.joinpath('markdown.md')) as f:
        return f.readlines()


@pytest.fixture
def html_page(plugin_environment, diagrams_dict):
    page = MagicMock(title='Test, page', file=MagicMock(), config=MagicMock())
    template = plugin_environment.get_template("output.html")
    page.content = template.render(
        uuid_class=PlantUMLPlugin.pre_class_name,
        uuids=diagrams_dict.keys()
    )
    page.html = page.content
    return page
