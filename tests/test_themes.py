from mkdocs_puml.themes import Theme


def test_theme(diagram_and_encoded: tuple[str, str]):
    url = "example.url"
    name = "default/light"
    theme = Theme(url=url)
    with_theme = theme.include(name, diagram_and_encoded[0]).split("\n")

    assert with_theme[1] == f"!include {url}/{name}.puml"


def test_without_startuml():
    diagram = "Bob -> Alice"
    url = "example.url"
    name = "default/light"
    theme = Theme(url=url)

    with_theme = theme.include(name, diagram).split("\n")

    assert with_theme[0] == f"!include {url}/{name}.puml"


def test_with_c4(c4_diagram: str):
    url = "example.url"
    name = "default/light"
    theme = Theme(url=url)

    with_theme = theme.include(name, c4_diagram).split("\n")

    # strip because c4_diagram uses raw-formatted strings
    assert with_theme[1].strip() == "!include https://raw.git.../C4-PlantUML/master/C4_Container.puml"
    assert with_theme[2].strip() == f"!include {url}/{name}.puml"
