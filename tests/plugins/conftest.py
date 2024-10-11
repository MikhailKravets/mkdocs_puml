import uuid
from unittest.mock import MagicMock

import jinja2
import pytest

from uuid import UUID

from mkdocs_puml.configs import CacheConfig, LocalCacheConfig, PlantUMLConfig, ThemeConfig
from mkdocs_puml.model import ThemeMode
from mkdocs_puml.plugin import Diagram, PlantUMLPlugin
from tests.conftest import BASE_PUML_URL, TESTDATA_DIR


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


def patch_plugin_to_single_theme(plugin: PlantUMLPlugin):
    plugin.config.theme.enabled = False
    plugin.themer = None
    plugin.theme_light = None
    plugin.theme_dark = None


@pytest.fixture
def plugin_config() -> PlantUMLConfig:
    c = PlantUMLConfig()

    t = ThemeConfig()
    t.load_dict({"light": "default/light", "dark": "default/dark", "url": "test.url/themes"})

    cache = CacheConfig()
    cache.load_dict({"backend": "disabled", "local": LocalCacheConfig()})
    c.load_dict(
        {
            "puml_url": BASE_PUML_URL,
            "extra_css": [],
            "theme": t,
            "cache": cache
        }
    )
    return c


@pytest.fixture
def plugin_environment():
    loader = jinja2.FileSystemLoader(searchpath=TESTDATA_DIR)
    return jinja2.Environment(loader=loader)


@pytest.fixture
def plant_uml_plugin(plugin_config):
    plugin = PlantUMLPlugin()
    plugin.config = plugin_config
    plugin.on_config(plugin_config)

    return plugin


@pytest.fixture
def diagrams_dict(diagram_and_encoded):
    return {
        str(uuid.uuid4()): Diagram(diagram_and_encoded[0], mode=ThemeMode.LIGHT),
        str(uuid.uuid4()): Diagram(diagram_and_encoded[0], mode=ThemeMode.DARK),
        str(uuid.uuid4()): Diagram(diagram_and_encoded[0], mode=ThemeMode.LIGHT),
    }


@pytest.fixture(scope="package")
def md_lines():
    with open(TESTDATA_DIR.joinpath("markdown.md")) as f:
        return f.readlines()


@pytest.fixture
def html_page(plugin_environment, diagrams_dict):
    page = MagicMock(title="Test, page", file=MagicMock(), config=MagicMock())
    template = plugin_environment.get_template("output.html")
    page.content = template.render(
        uuid_class=PlantUMLPlugin.pre_class_name, uuids=diagrams_dict.keys()
    )
    page.html = page.content
    return page
