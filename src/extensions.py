import re

from markdown import Markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

from src import PlantUML


class PumlExtension(Extension):
    """PUML Extension for Python-Markdown."""
    def __init__(self, name, puml_url):
        self.name = name
        self.puml = PlantUML(puml_url, div_class=name)
        super().__init__()

    def extendMarkdown(self, md: Markdown):
        """ Insert PumlPreprocessor before FenceCodePreprocessor. """
        md.preprocessors.register(PumlPreprocessor(md, self.name, self.puml), 'puml', 26)


class PumlPreprocessor(Preprocessor):
    """
    Preprocessors are run after the text is broken into lines.

    Each preprocessor implements a "run" method that takes a pointer to a
    list of lines of the document, modifies it as necessary and returns
    either the same pointer or a pointer to a new list.

    Preprocessors must extend markdown.Preprocessor.

    """
    def __init__(self, md, name, puml):
        self.name = name
        self.puml = puml
        self.regex = re.compile(rf"```{name}(.+?)```", flags=re.DOTALL)
        super().__init__(md)

    def run(self, lines):
        text = '\n'.join(lines)
        schemes = {}
        for scheme in self.regex.findall(text):
            converted = self.puml.translate(scheme)
            schemes[f"```{self.name}{scheme}```"] = converted

        for k, v in schemes.items():
            text = text.replace(k, v)

        return text.split('\n')


def makeExtension(**kwargs):
    return PumlExtension(**kwargs)
