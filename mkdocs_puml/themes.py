import re
from mkdocs_puml.utils import sanitize_url

C4_REGEX = re.compile(r"(!include(?:.+)(?:[Cc]4)(?:.+).puml)")


class Theme:
    """Theme class helps integrate available themes into PlantUML code.

    Theme includes theme url after all C4 inclusions. It makes possible
    to provide custom styling to C4 code as well.

    Args:
        url (str): repository of themes
    """

    def __init__(self, url: str):
        self.url = sanitize_url(url)

    def include(self, theme: str, diagram: str) -> str:
        """Includes theme to the beginning of PlantUML diagram

        Args:
            theme (str): theme name to include
            diagram (str): diagram into which to include

        Returns:
            str: PlantUML diagram with theme included
        """
        diagram = diagram.strip()
        with_c4 = C4_REGEX.split(diagram)
        url = self.url_for(theme)

        if len(with_c4) == 1:
            if diagram.startswith("@startuml"):
                head, _, tail = diagram.partition("\n")
            else:
                head, tail = None, diagram

            if head:
                return f"{head}\n!include {url}\n{tail}"
            return f"!include {url}\n{tail}"
        else:
            tail = with_c4[-1]
            with_c4[-1] = f"\n!include {url}"
            with_c4.append(tail)
            return "".join(with_c4)

    def url_for(self, theme: str) -> str:
        """Create full url for theme

        Args:
            theme (str): theme name

        Returns:
            str: full url for theme
        """
        return f"{self.url}{theme}.puml"
