from mkdocs.config.config_options import Config

from mkdocs_puml.plugins import PlantUMLPlugin
from mkdocs_puml.puml import PlantUML
from tests.conftest import BASE_PUML_URL
from tests.plugins.conftest import is_uuid_valid


def test_on_config():
    plugin = PlantUMLPlugin()

    # TODO: move Config creation into fixtures
    c = Config(schema=plugin.config_scheme)
    c['puml_url'] = BASE_PUML_URL
    plugin.config = c

    plugin.on_config(c)

    assert isinstance(plugin.puml, PlantUML)
    assert plugin.puml.base_url == BASE_PUML_URL


def test_on_page_markdown(plant_uml_plugin, md_lines):
    plant_uml_plugin.on_page_markdown("\n".join(md_lines))

    assert len(plant_uml_plugin.diagrams) == 2

    for key in plant_uml_plugin.diagrams.keys():
        assert is_uuid_valid(key)

    for val in plant_uml_plugin.diagrams.values():
        assert "@startuml" in val and "@enduml" in val


def test_on_env(plant_uml_plugin, mock_requests, md_lines):
    # TODO: add md_lines to diagrams
    # TODO: check that all were converted
    # TODO: check that for all diagram request were made
    pass


def test_on_post_page():
    pass
