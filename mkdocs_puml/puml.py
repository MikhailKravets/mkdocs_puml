import re
from urllib.parse import urljoin
from xml.dom.minidom import Element, parseString  # nosec

import requests

from mkdocs_puml.encoder import encode


class PlantUML:
    """PlantUML converter class.
    It requests PUML service, updates received `svg`
    and returns to the user.

    Attributes:
        base_url (str): Base URL to the PUML service
        _format (str): The format of build diagram. Used in the requesting URL
        _html_comment_regex (re.Pattern): Regex pattern to remove html comments from received svg

    Examples:
        Use this class as::

            puml = PlantUML("https://www.plantuml.com")
            svg = puml.translate(diagram)
    """
    _format = 'svg'
    _html_comment_regex = re.compile(r"<!--.*?-->", flags=re.DOTALL)

    def __init__(self, base_url: str):
        self.base_url = base_url if base_url.endswith('/') else f"{base_url}/"

    def translate(self, content: str) -> str:
        """Translate string diagram into HTML div
        block containing the received SVG image.

        Examples:
                This method translates content
                into <svg> image of the diagram

        Args:
            content (str): string representation of PUML diagram
        Returns:
             SVG image of built diagram
        """
        encoded = encode(content)
        resp = requests.get(urljoin(self.base_url, f"{self._format}/{encoded}"))
        diagram_content = resp.content.decode('utf-8')
        diagram_content = self._clean_comments(diagram_content)

        svg = self._convert_to_dom(diagram_content)
        self._stylize_svg(svg)

        return svg.toxml()

    def _clean_comments(self, content: str) -> str:
        return self._html_comment_regex.sub("", content)

    def _convert_to_dom(self, content: str) -> Element:
        """The method to convert received SVG into XML DOM
        for future modifications
        """
        dom = parseString(content)  # nosec
        svg = dom.getElementsByTagName('svg')[0]
        return svg

    def _stylize_svg(self, svg: Element):
        """This method is used for SVG tags modifications.

        Notes:
            It can be used to add support of light / dark theme.
        """
        svg.setAttribute('preserveAspectRatio', "true")
        svg.setAttribute('style', 'background: #ffffff')
