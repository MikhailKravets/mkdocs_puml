from mkdocs_puml.themes import Theme


def test_theme(diagram_and_encoded: tuple[str, str]):
    url = "example.url"
    name = "default/light"
    theme = Theme(url=url)
    with_theme = theme.include(name, diagram_and_encoded[0]).split("\n")

    assert with_theme[1] == f"!include {url}/{name}.puml"


def test_from_github(diagram_and_encoded: tuple[str, str]):
    name = "default/light"
    maintainer = "test"
    branch = "default"
    theme = Theme.from_github(maintainer, branch)

    with_theme = theme.include(name, diagram_and_encoded[0]).split("\n")

    assert (
        with_theme[1]
        == f"!include https://raw.githubusercontent.com/{maintainer}/mkdocs_puml/{branch}/themes/{name}.puml"
    )


def test_without_startuml():
    diagram = "Bob -> Alice"
    url = "example.url"
    name = "default/light"
    theme = Theme(url=url)

    with_theme = theme.include(name, diagram).split("\n")

    assert with_theme[0] == f"!include {url}/{name}.puml"
