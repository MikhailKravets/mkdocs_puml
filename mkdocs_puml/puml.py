import asyncio
from dataclasses import dataclass
import logging
import typing
import re

from urllib.parse import urljoin
from xml.dom.minidom import Element, parseString  # nosec

from httpx import AsyncClient, Response

from mkdocs_puml.encoder import encode
from mkdocs_puml.utils import sanitize_url


logger = logging.getLogger("mkdocs.plugins.plantuml")


@dataclass
class Fallback:
    """Fallback message for a scheme when PlantUML returns an error"""

    status_code: int
    message: str

    def __str__(self):  # pragma: no cover
        return f"{self.status_code}. {self.message}"


class PlantUML:
    """PlantUML converter class.
    It requests PUML service, updates received `svg`
    and returns it to the user.

    Attributes:
        base_url (str): Base URL to the PUML service
        num_workers (int): The size of pool to run requests in
        verify_ssl (bool): Designates whether the ``requests`` should verify SSL certiticate
        output_format (str): The output format for the diagrams (e.g., "svg" or "dsvg")

    Examples:
        Use this class as::

            puml = PlantUML("https://www.plantuml.com")
            svg = puml.translate([diagram])[0]
    """

    _html_comment_regex = re.compile(r"<!--.*?-->", flags=re.DOTALL)

    def __init__(
        self,
        base_url: str,
        verify_ssl: bool = True,
        output_format: str = "svg",
        timeout: int = 40,
    ):
        # Use sanitize_url because urllib removes last part of url which doesn't
        # end with / which makes it inconvenient to work with.
        self.base_url = sanitize_url(base_url)
        self.base_url = f"{self.base_url}{output_format}/"

        self.verify_ssl = verify_ssl
        self.timeout = timeout

    def translate(self, schemes: typing.Iterable[str]) -> typing.List[str]:
        """Translate PlantUML schemes into the received SVG image.

        Args:
            schemes (list): string representation of PUML diagram

        Returns:
            SVG image of built diagram
        """
        encoded = [self.preprocess(v) for v in schemes]

        svg_images = self.request(encoded)

        for i, v in enumerate(svg_images):
            svg_images[i] = self.postprocess(v)

        return svg_images

    def preprocess(self, content: str) -> str:
        """Pre-process the content before passing it
        to the PlantUML service.

        Encoding of the content should be
        done in the step of preprocessing.

        Args:
            content (str): string representation PUML diagram
        Returns:
            Encoded and pre-processed PUML diagram
        """
        return encode(content)

    def postprocess(self, content: typing.Union[str, Fallback]) -> str:
        """Postprocess an SVG diagram received from PlantUML server.

        The code that applies CSS styling to the SVG can be placed here.

        Args:
            content (str): SVG representation of build diagram
        Returns:
            Post-processed SVG diagram
        """
        if isinstance(content, Fallback):
            return str(content)

        diagram_content = self._clean_comments(content)

        svg = self._convert_to_dom(diagram_content)
        self._stylize_svg(svg)

        return svg.toxml()

    def request(self, schemes: list[str]) -> list[typing.Union[str, Fallback]]:
        """Request PlantUML service with the encoded diagram;
        return SVG content

        Args:
            schemes (str): Encoded string representation of the diagram diagrams
        Returns:
            SVG representation of the diagram
        """
        responses: list[Response] = asyncio.run(self._request_all(schemes))

        svgs = []
        for s, resp in zip(schemes, responses):
            # Use 'ignore' to strip non-utf chars
            c = resp.content.decode("utf-8", errors="ignore")
            if not resp.is_success:
                logger.warning(
                    f"While building diagram \n\n{s}\n\nServer responded"
                    f" with a status {resp.status_code}"
                )
                svgs.append(Fallback(status_code=resp.status_code, message=c))
            else:
                svgs.append(c)

        return svgs

    async def _request_one(self, uri: str) -> Response:
        """Request request PlantUML server asynchronously

        Args:
            uri (str): URI with encoded diagram attached to it

        Returns:
            Response: response from PlantUML server
        """
        async with AsyncClient(verify=self.verify_ssl, timeout=self.timeout) as client:
            return await client.get(uri)

    async def _request_all(self, schemes: list[str]):
        """Asynchronous wrapper that creates request coroutine for
        each scheme and after await returns an ordered list of responses.

        Args:
            schemes (list[str]): encoded PlantUML diagrams

        Returns:
            list[Response]: ordered list of Responses
        """
        return await asyncio.gather(
            *(self._request_one(urljoin(self.base_url, v)) for v in schemes)
        )

    def _clean_comments(self, content: str) -> str:
        """Remove comments from HTML content"""
        return self._html_comment_regex.sub("", content)

    def _convert_to_dom(self, content: str) -> Element:
        """The method to convert received SVG into XML DOM
        for future modifications
        """
        dom = parseString(content)  # nosec
        svg = dom.getElementsByTagName("svg")[0]
        return svg

    def _stylize_svg(self, svg: Element):
        """This method is used for SVG tags modifications"""
        svg.setAttribute("preserveAspectRatio", "xMidYMid meet")
        svg.setAttribute("style", "background: var(--md-default-bg-color)")
