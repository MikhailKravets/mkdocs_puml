import typing
import re
import uuid

from mkdocs.config.config_options import Type, Config
from mkdocs.plugins import BasePlugin

from mkdocs_puml.puml import PlantUML


class PlantUMLPlugin(BasePlugin):
    """MKDocs plugin that converts puml diagrams into inline SVG images.

    It works with remote PlantUML service only. You should add
    these configs into ``mkdocs.yml``::

            plugins:
                - mkdocs_puml:
                    puml_url: https://www.plantuml.com/plantuml
                    num_worker: 10

    Attributes:
        div_class_name (str): the class that will be set to resulting <div> tag
                              containing the diagram
        pre_class_name (str): the class that will be set to intermediate <pre> tag
                              containing uuid code
        config_scheme (str): config scheme to set by user in mkdocs.yml file

        regex (re.Pattern): regex to find all puml code blocks
        uuid_regex (re.Pattern): regex to find all uuid <pre> blocks
        puml (PlantUML): PlantUML instance that requests PlantUML service
        diagrams (dict): Dictionary containing the diagrams (puml and later svg) and their keys
    """
    div_class_name = "puml"
    pre_class_name = "diagram-uuid"

    config_scheme = (
        ('puml_url', Type(str, required=True)),
        ('num_worker', Type(int, default=8))
    )

    def __init__(self):
        self.regex = re.compile(rf"```{self.div_class_name}(.+?)```", flags=re.DOTALL)
        self.uuid_regex = re.compile(rf'<pre class="{self.pre_class_name}">(.+?)</pre>', flags=re.DOTALL)

        self.puml: typing.Optional[PlantUML] = None
        self.diagrams = {
            # key - uuid: value - puml. After on_env — svg
        }

    def on_config(self, config: Config) -> Config:
        """Event that is run by mkdocs when configs are created.

        self.puml instance is populated in this event.

        Args:
            config: Full mkdocs.yml config file. To access configs of PlantUMLPlugin only,
                    use self.config attribute.

        Returns:
            Full config of the mkdocs
        """
        self.puml = PlantUML(self.config['puml_url'], num_worker=self.config['num_worker'])
        return config

    def on_page_markdown(self, markdown: str, *args, **kwargs) -> str:
        """Event to fire for each .md page.

        Here, all ``puml`` code blocks are found and added to self.diagrams
        with the corresponding uuid key.

        Then, <pre class="...">uuid of diagram</pre> tags are added to
        the markdown page.

        Args:
            markdown: Markdown page in which to look for ``puml`` diagrams.

        Returns:
            Updated markdown page
        """
        schemes = self.regex.findall(markdown)

        for v in schemes:
            id_ = str(uuid.uuid4())
            self.diagrams[id_] = v
            markdown = markdown.replace(
                f"```{self.div_class_name}{v}```",
                f'<pre class="{self.pre_class_name}">{id_}</pre>'
            )

        return markdown

    def on_env(self, env, *args, **kwargs):
        """The event is fired when jinja environment is configured.
        Such as it is fired once when all .md pages are processed,
        we can use it to request PlantUML service to convert our
        diagrams.

        Args:
            env: jinja environment
        Returns:
            Jinja environment
        """
        resp = self.puml.translate(self.diagrams.values())

        for key, svg in zip(self.diagrams.keys(), resp):
            self.diagrams[key] = svg
        return env

    def on_post_page(self, output: str, *args, **kwargs) -> str:
        """The event is fired after HTML page is rendered.
        Here, we substitute <pre> tags with uuid codes of diagrams
        with the corresponding SVG images.

        Args:
            output: rendered HTML page

        Returns:
            HTML page containing SVG diagrams
        """
        schemes = self.uuid_regex.findall(output)
        for v in schemes:
            output = output.replace(
                f'<pre class="{self.pre_class_name}">{v}</pre>',
                f'<div class="{self.div_class_name}">{self.diagrams[v]}</div>'
            )
        return output
