import typing
import re
import uuid

from mkdocs.config.config_options import Type, Config
from mkdocs.plugins import BasePlugin

from mkdocs_puml.puml import PlantUML


class PlantUMLPlugin(BasePlugin):
    name = "puml"
    pre_class_name = "diagram-uuid"

    config_scheme = (
        ('puml_url', Type(str, required=True)),
        ('num_worker', Type(int, default=8))
    )

    def __init__(self):
        self.regex = re.compile(rf"```{self.name}(.+?)```", flags=re.DOTALL)
        self.uuid_regex = re.compile(rf'<pre class="{self.pre_class_name}">(.+?)</pre>', flags=re.DOTALL)

        self.puml: typing.Optional[PlantUML] = None
        self.diagrams = {
            # key - uuid: value - puml or [puml, svg]
        }

    def on_config(self, config: Config):
        self.puml = PlantUML(self.config['puml_url'], num_worker=self.config['num_worker'])
        return config

    def on_page_markdown(self, markdown: str, *args, **kwargs):  # page: Page, config: Config, files: Files
        schemes = self.regex.findall(markdown)

        for v in schemes:
            id_ = str(uuid.uuid4())
            self.diagrams[id_] = v
            markdown = markdown.replace(f"```{self.name}{v}```", f'<pre class="uuid">{id_}</pre>')

        return markdown

    def on_env(self, env, *args, **kwargs):  # config: Config, files: Files
        resp = self.puml.translate(self.diagrams.values())

        for key, svg in zip(self.diagrams.keys(), resp):
            self.diagrams[key] = svg
        return env

    def on_post_page(self, output: str, *args, **kwargs):  # page: Page, config: Config
        schemes = self.uuid_regex.findall(output)
        for v in schemes:
            output = output.replace(
                f'<pre class="{self.pre_class_name}">{v}</pre>',
                f'<div class="{self.name}">{self.diagrams[v]}</div>'
            )
        return output
