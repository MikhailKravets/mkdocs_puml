from mkdocs_puml.plugin import PlantUMLPlugin
from mkdocs_puml.puml import PlantUML
from tests.conftest import BASE_PUML_KEYWORD, BASE_PUML_URL, CUSTOM_PUML_KEYWORD
from tests.plugins.conftest import is_uuid_valid


def test_on_config(plugin_config):
    plugin = PlantUMLPlugin()
    plugin.config = plugin_config

    plugin.on_config(plugin_config)

    assert isinstance(plugin.puml, PlantUML)
    assert plugin.puml.base_url == BASE_PUML_URL
    assert plugin.puml_keyword == BASE_PUML_KEYWORD


def test_on_config_custom_keyword(plugin_config_custom_keyword):
    plugin = PlantUMLPlugin()
    plugin.config = plugin_config_custom_keyword

    plugin.on_config(plugin_config_custom_keyword)

    assert isinstance(plugin.puml, PlantUML)
    assert plugin.puml.base_url == BASE_PUML_URL
    assert plugin.puml_keyword == CUSTOM_PUML_KEYWORD


def test_on_page_markdown(plant_uml_plugin, md_lines):
    plant_uml_plugin.on_page_markdown("\n".join(md_lines))

    assert len(plant_uml_plugin.diagrams) == 2

    for key in plant_uml_plugin.diagrams.keys():
        assert is_uuid_valid(key)

    for val in plant_uml_plugin.diagrams.values():
        assert "@startuml" in val and "@enduml" in val


def test_on_page_markdown_custom_keyword(plant_uml_plugin_custom_keyword, md_lines):
    plant_uml_plugin_custom_keyword.on_page_markdown("\n".join(md_lines))

    assert len(plant_uml_plugin_custom_keyword.diagrams) == 1

    for key in plant_uml_plugin_custom_keyword.diagrams.keys():
        assert is_uuid_valid(key)

    for val in plant_uml_plugin_custom_keyword.diagrams.values():
        assert "@startuml" in val and "@enduml" in val


def test_on_env(mock_requests, plant_uml_plugin, diagrams_dict, plugin_environment):
    plant_uml_plugin.diagrams = diagrams_dict
    plant_uml_plugin.on_env(plugin_environment)

    assert mock_requests.call_count == len(diagrams_dict)

    for v in diagrams_dict.values():
        assert v.startswith('<svg')


def test_on_post_page(plant_uml_plugin, diagrams_dict, html_page):
    plant_uml_plugin.diagrams = diagrams_dict
    output = plant_uml_plugin.on_post_page(html_page.content, html_page)

    assert output.count(f'<div class="{plant_uml_plugin.div_class_name}">') == len(diagrams_dict)
