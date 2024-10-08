from mkdocs_puml.plugin import PlantUMLPlugin, ThemeMode
from mkdocs_puml.puml import PlantUML
from mkdocs_puml.themes import Theme
from tests.conftest import BASE_PUML_KEYWORD, CUSTOM_PUML_KEYWORD
from tests.plugins.conftest import is_uuid_valid, patch_plugin_to_single_theme


def test_on_config(plugin_config):
    # Test if the plugin is correctly configured with default settings
    plugin = PlantUMLPlugin()
    plugin.config = plugin_config

    plugin.on_config(plugin_config)

    assert isinstance(plugin.puml, PlantUML)
    assert isinstance(plugin.themer, Theme)

    assert plugin.theme_light == "default/light"
    assert plugin.theme_dark == "default/dark"
    assert plugin.puml_keyword == BASE_PUML_KEYWORD
    assert "assets/stylesheets/puml.css" in plugin_config["extra_css"]


def test_on_config_custom_keyword(plugin_config_custom_keyword):
    # Test if the plugin is correctly configured with a custom keyword
    plugin = PlantUMLPlugin()
    plugin.config = plugin_config_custom_keyword

    plugin.on_config(plugin_config_custom_keyword)

    assert plugin.puml_keyword == CUSTOM_PUML_KEYWORD


def test_on_page_markdown_single_theme(plant_uml_plugin, md_lines):
    patch_plugin_to_single_theme(plant_uml_plugin)

    plant_uml_plugin.on_page_markdown("\n".join(md_lines))

    assert len(plant_uml_plugin.diagrams) == 2

    for key in plant_uml_plugin.diagrams:
        assert is_uuid_valid(key)

    for val in plant_uml_plugin.diagrams.values():
        assert "@startuml" in val.scheme and "@enduml" in val.scheme


def test_on_page_markdown_dual_themes(plant_uml_plugin, md_lines):
    plant_uml_plugin.on_page_markdown("\n".join(md_lines))

    assert len(plant_uml_plugin.diagrams) == 4

    for key, val in plant_uml_plugin.diagrams.items():
        if val.mode == ThemeMode.LIGHT:
            assert is_uuid_valid(key)
        else:
            uuid_key, _, dark = key.rpartition("-")
            assert is_uuid_valid(uuid_key)
            assert dark == "dark"

    for val in plant_uml_plugin.diagrams.values():
        assert "@startuml" in val.scheme and "@enduml" in val.scheme


def test_on_page_markdown_custom_keyword(plant_uml_plugin_custom_keyword, md_lines):
    # Test if PlantUML diagrams are correctly extracted with a custom keyword
    plant_uml_plugin_custom_keyword.on_page_markdown("\n".join(md_lines))

    assert len(plant_uml_plugin_custom_keyword.diagrams) == 2


def test_on_env(mock_requests, plant_uml_plugin, diagrams_dict, plugin_environment):
    # Test if PlantUML diagrams are correctly converted to SVG
    plant_uml_plugin.diagrams = diagrams_dict
    plant_uml_plugin.on_env(plugin_environment)

    assert mock_requests.call_count == len(diagrams_dict)

    for diagram in plant_uml_plugin.diagrams.values():
        assert diagram.diagram.startswith("<svg")


def test_on_post_page(plant_uml_plugin, diagrams_dict, html_page):
    plant_uml_plugin.diagrams = diagrams_dict
    output = plant_uml_plugin.on_post_page(html_page.content, html_page)

    assert output.count('<div class="puml light">') == len(
        [True for v in diagrams_dict.values() if v.mode == ThemeMode.LIGHT]
    )
    assert output.count('<div class="puml dark">') == len(
        [True for v in diagrams_dict.values() if v.mode == ThemeMode.DARK]
    )

    # Test the case where page.html exists
    # TODO: deprecated! After we raise mkdocs>=1.4 strictly, this will be never a case
    html_page.html = html_page.content
    output = plant_uml_plugin.on_post_page(html_page.content, html_page)
    assert html_page.html.count('<div class="puml light">') == len(
        [True for v in diagrams_dict.values() if v.mode == ThemeMode.LIGHT]
    )


def test_on_post_page_without_html_attribute(
    plant_uml_plugin, diagrams_dict, html_page
):
    # TODO: deprecated! After we raise mkdocs>=1.4 strictly, this will be never a case
    plant_uml_plugin.diagrams = diagrams_dict
    delattr(html_page, "html")
    output = plant_uml_plugin.on_post_page(html_page.content, html_page)

    assert output.count('<div class="puml light">') == len(
        [True for v in diagrams_dict.values() if v.mode == ThemeMode.LIGHT]
    )


def test_on_post_build(tmp_path, plant_uml_plugin):
    # Test if static files are correctly copied during the build process
    config = {"site_dir": str(tmp_path)}
    dest_dir = tmp_path.joinpath("assets/stylesheets")

    plant_uml_plugin.on_post_build(config)

    assert dest_dir.joinpath("puml.css").exists()


def test_on_post_build_with_subdirectory(tmp_path, plant_uml_plugin):
    # Test if the plugin correctly handles subdirectories in the static folder
    config = {"site_dir": str(tmp_path)}

    plant_uml_plugin.on_post_build(config)

    dest_dir = tmp_path.joinpath("assets/stylesheets")
    assert dest_dir.joinpath("puml.css").exists()
