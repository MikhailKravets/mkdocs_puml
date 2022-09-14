import re

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

from mkdocs_puml.puml import PlantUML


class PumlExtension(Extension):
    """PUML Extension for Python-Markdown"""
    def __init__(self, puml_url):
        self.puml = PlantUML(puml_url)
        super().__init__()

    def extendMarkdown(self, md: Markdown):
        """Insert PumlPreprocessor to markdown preprocessors.
        PumlPreprocessor should have higher priority than FenceCodePreprocessor
        """
        md.preprocessors.register(PumlPreprocessor(md, self.puml), 'puml', 26)


class PumlPreprocessor(Preprocessor):
    """Puml Preprocessor looks for all::

        ```puml
        ...
        ```

    blocks, requests plantUML service to build `svg`
    diagrams and substitutes them with the `svg` image.

    Attributes:
        md (Markdown): Markdown object
        puml (PlantUML): PlantUML converter class
    """
    name = "puml"

    def __init__(self, md, puml):
        self.puml = puml
        self.regex = re.compile(rf"```{self.name}(.+?)```", flags=re.DOTALL)
        super().__init__(md)

    def run(self, lines):
        text = '\n'.join(lines)
        schemes = {}
        for scheme in self.regex.findall(text):
            converted = self.puml.translate(scheme)
            schemes[f"```{self.name}{scheme}```"] = converted

        for k, v in schemes.items():
            text = text.replace(k, f'<div class="{self.name}">{v}</div>')

        return text.split('\n')


def makeExtension(**kwargs):
    return PumlExtension(**kwargs)
