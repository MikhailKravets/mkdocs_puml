import pytest

from uuid import UUID

from mkdocs.config.config_options import Config

from mkdocs_puml.plugins import PlantUMLPlugin
from tests.conftest import BASE_PUML_URL


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
def plant_uml_plugin(plugin_config):
    plugin = PlantUMLPlugin()
    c = Config(schema=plugin.config_scheme)
    c['puml_url'] = BASE_PUML_URL
    plugin.config = c
    plugin.on_config(c)

    return plugin
