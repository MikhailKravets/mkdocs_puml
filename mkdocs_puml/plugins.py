import typing

from mkdocs.config.config_options import Type, Config
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.plugins import BasePlugin

from mkdocs_puml.puml import PlantUML


class PlantUMLPlugin(BasePlugin):
    config_scheme = (
        ('puml_url', Type(str)),
        ('num_worker', Type(int, default=5))
    )

    def __init__(self):
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
        # TODO: findall in markdown
        # TODO: store to self.diagrams
        # TODO: replace puml to uuid in markdown string
        return markdown

    def on_env(self, env, config: Config, files: Files):
        print("On env")
        # TODO: call self.puml.translate with the self.diagrams.values()
        return env

    def on_post_page(self, output, page: Page, config: Config):
        print("On post page")
        # TODO: fina all uuid in output and replace
        #  with the corresponding diagram
        return output
