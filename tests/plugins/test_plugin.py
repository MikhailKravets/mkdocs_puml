from mkdocs_puml.plugin import PlantUMLPlugin
from mkdocs_puml.puml import PlantUML
from tests.conftest import BASE_PUML_KEYWORD, BASE_PUML_URL, CUSTOM_PUML_KEYWORD
from tests.plugins.conftest import is_uuid_valid
import os
import shutil


def test_on_config(plugin_config):
    # Test if the plugin is correctly configured with default settings
    plugin = PlantUMLPlugin()
    plugin.config = plugin_config

    plugin.on_config(plugin_config)

    assert isinstance(plugin.puml_light, PlantUML)
    assert isinstance(plugin.puml_dark, PlantUML)
    assert plugin.puml_light.base_url == BASE_PUML_URL + "svg/"
    assert plugin.puml_dark.base_url == BASE_PUML_URL + "dsvg/"
    assert plugin.puml_keyword == BASE_PUML_KEYWORD


def test_on_config_custom_keyword(plugin_config_custom_keyword):
    # Test if the plugin is correctly configured with a custom keyword
    plugin = PlantUMLPlugin()
    plugin.config = plugin_config_custom_keyword

    plugin.on_config(plugin_config_custom_keyword)

    assert isinstance(plugin.puml_light, PlantUML)
    assert isinstance(plugin.puml_dark, PlantUML)
    assert plugin.puml_light.base_url == BASE_PUML_URL + "svg/"
    assert plugin.puml_dark.base_url == BASE_PUML_URL + "dsvg/"
    assert plugin.puml_keyword == CUSTOM_PUML_KEYWORD


def test_on_page_markdown(plant_uml_plugin, md_lines):
    # Test if PlantUML diagrams are correctly extracted from markdown
    plant_uml_plugin.on_page_markdown("\n".join(md_lines))

    assert len(plant_uml_plugin.diagrams) == 2

    for key in plant_uml_plugin.diagrams.keys():
        assert is_uuid_valid(key)

    for val in plant_uml_plugin.diagrams.values():
        assert "@startuml" in val and "@enduml" in val


def test_on_page_markdown_custom_keyword(plant_uml_plugin_custom_keyword, md_lines):
    # Test if PlantUML diagrams are correctly extracted with a custom keyword
    plant_uml_plugin_custom_keyword.on_page_markdown("\n".join(md_lines))

    assert len(plant_uml_plugin_custom_keyword.diagrams) == 1

    for key in plant_uml_plugin_custom_keyword.diagrams.keys():
        assert is_uuid_valid(key)

    for val in plant_uml_plugin_custom_keyword.diagrams.values():
        assert "@startuml" in val and "@enduml" in val


def test_on_env(mock_requests, plant_uml_plugin, diagrams_dict, plugin_environment):
    # Test if PlantUML diagrams are correctly converted to SVG
    plant_uml_plugin.diagrams = diagrams_dict
    plant_uml_plugin.on_env(plugin_environment)

    assert mock_requests.call_count == len(diagrams_dict)

    for light_svg, dark_svg in plant_uml_plugin.diagrams.values():
        assert isinstance(light_svg, str)
        assert light_svg.startswith("<svg")
        assert dark_svg is None  # Since auto_dark is False by default


def test_on_env_auto_dark(mock_requests, plant_uml_plugin, diagrams_dict, plugin_environment):
    # Test if PlantUML diagrams are correctly converted to both light and dark SVGs
    plant_uml_plugin.auto_dark = True
    plant_uml_plugin.diagrams = diagrams_dict
    mock_requests.reset_mock()
    plant_uml_plugin.on_env(plugin_environment)

    assert mock_requests.call_count == 2 * len(diagrams_dict)

    for light_svg, dark_svg in plant_uml_plugin.diagrams.values():
        assert isinstance(light_svg, str)
        assert isinstance(dark_svg, str)
        assert light_svg.startswith("<svg")
        assert dark_svg.startswith("<svg")


def test_on_post_page(plant_uml_plugin, diagrams_dict, html_page):
    # Test if PlantUML diagrams are correctly inserted into the HTML output
    plant_uml_plugin.diagrams = diagrams_dict
    output = plant_uml_plugin.on_post_page(html_page.content, html_page)

    assert output.count(f'<div class="{plant_uml_plugin.div_class_name}">') == len(diagrams_dict)
    assert '<script src="assets/javascripts/puml/dark.js"></script>' in output

    # Test the case where page.html exists
    html_page.html = html_page.content
    output = plant_uml_plugin.on_post_page(html_page.content, html_page)
    assert html_page.html.count(f'<div class="{plant_uml_plugin.div_class_name}">') == len(
        diagrams_dict
    )


def test_on_post_page_without_html_attribute(plant_uml_plugin, diagrams_dict, html_page):
    # Test if the plugin handles pages without the 'html' attribute correctly
    plant_uml_plugin.diagrams = diagrams_dict
    delattr(html_page, "html")
    output = plant_uml_plugin.on_post_page(html_page.content, html_page)

    assert output.count(f'<div class="{plant_uml_plugin.div_class_name}">') == len(diagrams_dict)
    assert '<script src="assets/javascripts/puml/dark.js"></script>' in output


def test_on_post_page_with_existing_script(plant_uml_plugin, diagrams_dict, html_page):
    # Test if the plugin doesn't duplicate the script tag when it already exists
    plant_uml_plugin.diagrams = diagrams_dict
    html_page.content += '<script src="assets/javascripts/puml/dark.js"></script>'
    output = plant_uml_plugin.on_post_page(html_page.content, html_page)

    assert output.count('<script src="assets/javascripts/puml/dark.js"></script>') == 1


def test_on_post_build(tmp_path, plant_uml_plugin):
    # Test if static files are correctly copied during the build process
    config = {"site_dir": str(tmp_path)}

    dest_dir = os.path.join(tmp_path, "assets", "javascripts", "puml")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    plant_uml_plugin.on_post_build(config)

    assert os.path.exists(dest_dir)
    static_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "mkdocs_puml", "static"
    )
    for file_name in os.listdir(static_dir):
        assert os.path.exists(os.path.join(dest_dir, file_name))

    # Test when the directory already exists
    plant_uml_plugin.on_post_build(config)

    for file_name in os.listdir(static_dir):
        assert os.path.exists(os.path.join(dest_dir, file_name))


def test_on_post_build_with_subdirectory(tmp_path, plant_uml_plugin):
    # Test if the plugin correctly handles subdirectories in the static folder
    config = {"site_dir": str(tmp_path)}

    plant_uml_plugin.on_post_build(config)

    dest_dir = os.path.join(tmp_path, "assets", "javascripts", "puml")
    for item in os.listdir(dest_dir):
        assert os.path.isfile(os.path.join(dest_dir, item))


def test_replace_method(plant_uml_plugin):
    # Test if the _replace method correctly handles both light and dark SVGs
    key = "test_key"
    content = f'<pre class="{plant_uml_plugin.pre_class_name}">{key}</pre>'

    # Test without dark SVG
    plant_uml_plugin.diagrams[key] = ("<svg>light</svg>", None)
    result = plant_uml_plugin._replace(key, content)
    assert f'<div class="{plant_uml_plugin.div_class_name}"><svg>light</svg></div>' in result

    # Test with dark SVG
    plant_uml_plugin.diagrams[key] = ("<svg>light</svg>", "<svg>dark</svg>")
    result = plant_uml_plugin._replace(key, content)
    assert 'data-puml-theme="light"' in result
    assert 'data-puml-theme="dark"' in result
    assert "<svg>light</svg>" in result
    assert "<svg>dark</svg>" in result
