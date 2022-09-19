import typing
import re
import uuid

from mkdocs.config.config_options import Type, Config
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.plugins import BasePlugin

from mkdocs_puml.puml import PlantUML


class PlantUMLPlugin(BasePlugin):
    name = "puml"
    config_scheme = (
        ('puml_url', Type(str, required=True)),
        ('num_worker', Type(int, default=8))
    )

    def __init__(self):
        self.regex = re.compile(rf"```{self.name}(.+?)```", flags=re.DOTALL)
        self.uuid_regex = re.compile(r'<pre class="uuid">(.+?)</pre>', flags=re.DOTALL)

        self.puml: typing.Optional[PlantUML] = None
        self.diagrams = {
            # key - uuid: value - puml or [puml, svg]
        }
        print("Init is called")

    def on_config(self, config: Config):
        print("Config is called")
        self.puml = PlantUML(self.config['puml_url'], num_worker=self.config['num_worker'])
        return config

    def on_pre_build(self, config: Config):
        print("On pre-build is called")
        return config

    def on_files(self, files: Files, config: Config):
        print("On files")
        return files

    def on_page_markdown(self, markdown: str, page: Page, config: Config, files: Files):
        print("On page markdown")
        schemes = self.regex.findall(markdown)

        for v in schemes:
            id_ = str(uuid.uuid4())
            self.diagrams[id_] = v
            markdown = markdown.replace(f"```{self.name}{v}```", f'<pre class="uuid">{id_}</pre>')

        return markdown

    def on_env(self, env, config: Config, files: Files):
        resp = self.puml.translate(self.diagrams.values())

        for key, svg in zip(self.diagrams.keys(), resp):
            self.diagrams[key] = svg
        return env

    def on_post_page(self, output, page: Page, config: Config):
        print("On post page")
        schemes = self.uuid_regex.findall(output)
        for v in schemes:
            output = output.replace(
                f'<pre class="uuid">{v}</pre>',
                f'<div class="{self.name}">{self.diagrams[v]}</div>'
            )
        return output
