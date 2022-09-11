import re
import requests

from xml.dom.minidom import Element, parseString
from urllib.parse import urljoin

from src.encoder import encode


class PlantUML:
    _format = 'plantuml/svg'
    _html_comment_regex = re.compile(r"<!--.*?-->", flags=re.DOTALL)

    def __init__(self, base_url: str, *, div_class: str = "puml"):
        self.base_url = base_url
        self.div_class = div_class

    def translate(self, content: str) -> str:
        """Translate string diagram into HTML div
        block containing the received SVG image.

        In the format::

            <div class="puml">
                ...SVG content...
            </div>

        :param content: string representation of PUML diagram
        :return: SVG image of built diagram
        """
        encoded = encode(content)
        resp = requests.get(urljoin(self.base_url, f"{self._format}/{encoded}"))
        diagram_content = resp.content.decode('utf-8')
        diagram_content = self._clean_comments(diagram_content)

        svg = self._convert_to_dom(diagram_content)
        self._stylize_svg(svg)

        return f'<div class="puml">{svg.toxml()}</div>'

    def _clean_comments(self, content: str) -> str:
        return self._html_comment_regex.sub("", content)

    def _convert_to_dom(self, content: str) -> Element:
        dom = parseString(content)
        svg = dom.getElementsByTagName('svg')[0]
        return svg

    def _stylize_svg(self, svg: Element):
        svg.setAttribute('preserveAspectRatio', "true")
        svg.removeAttribute('style')

