from mkdocs_puml.utils import sanitize_url


class Theme:
    """Theme class helps integrate available themes in diagrams

    Args:
        url (str): repository of themes
    """

    def __init__(self, url: str):
        self.url = sanitize_url(url)

    @classmethod
    def from_github(cls, maintainer: str, branch: str = "master"):
        """Create a URL of themes located in GitHub repository

        Args:
            maintainer (str): maintainer of the repository
            branch (str, optional): git branch with themes. Defaults to "master".

        Returns:
            str: URL to raw GitHub content
        """
        # TODO: is it ok to hardcode extension .puml??
        return cls(
            f"https://raw.githubusercontent.com/{maintainer}/mkdocs_puml/{branch}/themes/"
        )

    def include(self, theme: str, diagram: str) -> str:
        """Includes theme to the beginning of PlantUML diagram

        Args:
            theme (str): theme name to include
            diagram (str): diagram into which to include

        Returns:
            str: PlantUML diagram with theme included
        """
        diagram = diagram.strip()
        if diagram.startswith("@startuml"):
            head, _, tail = diagram.partition("\n")
        else:
            head, tail = None, diagram

        url = self.url_for(theme)

        if head:
            return f"{head}\n!include {url}\n{tail}"
        return f"!include {url}\n{tail}"

    def url_for(self, theme: str) -> str:
        """Create full url for theme

        Args:
            theme (str): theme name

        Returns:
            str: full url for theme
        """
        return f"{self.url}{theme}.puml"
