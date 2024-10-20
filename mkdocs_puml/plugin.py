from pathlib import Path
import typing
import re
import os
import shutil

from rich.console import Console

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin

from mkdocs_puml.config import PlantUMLConfig
from mkdocs_puml.model import Count, Diagram, ThemeMode
from mkdocs_puml.storage import AbstractStorage, build_storage
from mkdocs_puml.puml import Fallback, PlantUML
from mkdocs_puml.theme import Theme


class PlantUMLPlugin(BasePlugin[PlantUMLConfig]):
    """MKDocs plugin that converts puml diagrams into SVG images.

    It works only with a remote PlantUML service. You should add
    these configs into ``mkdocs.yml``::

            plugins:
                - mkdocs_puml:
                    puml_url: https://www.plantuml.com/plantuml

    The rest of configuration is optional. Please refer to plugin
    documentation to view them all

    Attributes:
        pre_class_name (str): the class that will be set to intermediate <pre> tag
                              containing uuid code
        container (str): html element where the diagrams will be inserted.
                         **DO NOT** insert any `\n` characters, as the Markdown parser will convert them into
                         `<p>...</p>`, which may result in an unexpected html
    """

    pre_class_name = "diagram-key"
    container = "<div class='puml-container'>{}</div>"

    def __init__(self):
        self.regex: typing.Optional[typing.Any] = None
        self.uuid_regex = re.compile(
            rf'<pre class="{self.pre_class_name}">(.+?)</pre>', flags=re.DOTALL
        )

        self.puml: typing.Optional[PlantUML] = None
        self.themer: typing.Optional[Theme] = None
        self.storage: typing.Optional[AbstractStorage] = None
        self.console: typing.Optional[Console] = None

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        """Event that is fired by mkdocs when configs are created.

        All required classes such as PlantUML, Theme, or any class for storage
        are initialized in this method.
        Also, `puml.css` file that enable dark / light mode styles is added to `extra_css`.

        Args:
            config: Full mkdocs.yml config file. To access configs of PlantUMLPlugin only,
                    use self.config attribute.

        Returns:
            Full config of the mkdocs
        """
        config["extra_css"].append("assets/mkdocs_puml/puml.css")
        config["extra_javascript"].append("assets/mkdocs_puml/puml.js")

        if self.config.interaction.enabled:
            config["extra_css"].append("assets/mkdocs_puml/interaction.css")
            config["extra_javascript"].extend(
                [
                    "https://unpkg.com/@panzoom/panzoom@4.5.1/dist/panzoom.min.js",
                    "assets/mkdocs_puml/interaction.js",
                ]
            )

        self.console = Console(quiet=not self.config.verbose)
        self.puml = PlantUML(
            self.config.puml_url,
            verify_ssl=self.config.verify_ssl,
            timeout=self.config.request_timeout
        )
        self.puml_keyword = self.config.puml_keyword
        self.regex = re.compile(rf"```{self.puml_keyword}(\n.+?)```", flags=re.DOTALL)

        if self.config.theme.enabled:
            self.themer = Theme(self.config.theme.url)

            self.theme_light = self.config.theme.light
            self.theme_dark = self.config.theme.dark
        else:
            self.themer = None
            self.theme_light = None
            self.theme_dark = None

        self.storage = build_storage(self.config.cache)

        return config

    def on_page_markdown(self, markdown: str, *args, **kwargs) -> str:
        """Event to fire for each .md page.

        Here, all ``puml`` code blocks are found and added to a storage.

        Then, <pre class="...">{key of diagram}</pre> tags are added to
        the markdown page.

        Args:
            markdown: Markdown page in which to look for PlantUML diagrams.

        Returns:
            Updated markdown page
        """
        with self.console.status(
            "[bold dim cyan]Search puml in markdown",
            spinner="dots2",
            spinner_style="magenta",
        ):
            schemes = self.regex.findall(markdown)

            # DO NOT insert `\n` characters in the replacement!
            for v in schemes:
                if self.themer:
                    replace_into = self.container.format(self._store_dual(v))
                else:
                    replace_into = self.container.format(self._store_single(v))
                markdown = markdown.replace(
                    f"```{self.puml_keyword}{v}```",
                    replace_into,
                )

        return markdown

    def _store_single(self, scheme: str) -> str:
        d = Diagram(scheme, mode=ThemeMode.LIGHT)
        key = self.storage.add(d)
        return f'<pre class="{self.pre_class_name}">{key}</pre>'

    def _store_dual(self, scheme: str) -> str:
        d_light = Diagram(
            self.themer.include(self.config.theme.light, scheme), mode=ThemeMode.LIGHT
        )
        d_dark = Diagram(
            self.themer.include(self.config.theme.dark, scheme), mode=ThemeMode.DARK
        )

        key_light = self.storage.add(d_light)
        key_dark = self.storage.add(d_dark)

        return (
            f'<pre class="{self.pre_class_name}">{key_light}</pre>'
            f'<pre class="{self.pre_class_name}">{key_dark}</pre>'
        )

    def on_env(self, env, *args, **kwargs):
        """The event is fired when jinja environment is configured.
        Such as it is fired once when all .md pages are processed,
        we can use it to request PlantUML service and convert the
        diagrams.

        Args:
            env: jinja environment
        Returns:
            Jinja environment
        """
        with self.console.status(
            "[bold dim cyan]Building PlantUML diagrams",
            spinner="dots2",
            spinner_style="magenta",
        ):
            to_request = self.storage.schemes()
            to_req_count = self.storage.count()
            svgs = self.puml.translate(to_request.values())
            self.storage.update(zip(to_request.keys(), svgs))

            fallback_count = len([True for v in svgs if isinstance(v, Fallback)])

        self.console.print(self._prepare_status_message(fallback_count, to_req_count))
        return env

    def on_post_page(self, output: str, page, *args, **kwargs) -> str:
        """The event is fired after HTML page is rendered.
        Here, we substitute <pre> tags with the corresponding SVG images.

        Args:
            output: rendered HTML in str format
            page: Page object

        Returns:
            HTML page containing SVG diagrams
        """
        schemes = self.uuid_regex.findall(output)
        for v in schemes:
            output = self._replace(v, output)
            page.content = output

        return output

    def on_post_build(self, config):
        """Event triggered after the build process is complete.

        This method copies static assets of the plugin and saves
        the diagrams to the storage.

        Args:
            config (dict): The MkDocs configuration object.

        """
        # Path to the static directory in the plugin
        static_dir = Path(__file__).parent.joinpath("static")
        # Destination directory in the site output
        dest_dir = Path(config["site_dir"]).joinpath("assets/mkdocs_puml/")

        if not dest_dir.exists():
            os.makedirs(dest_dir)

        # shutil.copy(static_dir, dest_dir)
        # shutil.copy(puml_js, dest_dir)
        shutil.copytree(static_dir, dest_dir, dirs_exist_ok=True)

        self.storage.save()

    def _replace(self, key: str, content: str) -> str:
        """Replace a key of a diagram with a diagram svg in a
        content
        """
        diagram = self.storage[key]

        # When theming is not enabled, user will manually manage themes in each diagram.
        # Also, only one version of diagram will be generated for each scheme, which
        # should be displayed always despite the light / dark mode of mkdocs-material.
        style = "display: block" if not self.config.theme.enabled else ""
        replacement = (
            f'<div class="puml {diagram.mode}" style="{style}">{diagram.diagram}</div>'
        )
        return content.replace(
            f'<pre class="{self.pre_class_name}">{key}</pre>', replacement
        )

    def _prepare_status_message(self, fallback_count: int, req_count: Count):
        if fallback_count:
            ok_msg = f".[/dim][bold red] {fallback_count} diagram failed to render ⨯[/bold red]"
        else:
            ok_msg = "[/dim] [green bold]✔️[/green bold]"

        if req_count.light == 0 and req_count.dark == 0:
            built_msg = "All diagrams loaded from cache"
        elif req_count.light == 0:
            d = "diagram" if req_count.dark == 1 else "diagrams"
            built_msg = f"Built {req_count.dark} dark {d}"
        elif req_count.dark == 0:
            d = "diagram" if req_count.light == 1 else "diagrams"
            built_msg = f"Built {req_count.light} light {d}"
        else:
            built_msg = f"Built {req_count.light} light and {req_count.dark} dark diagrams"

        return "[dim][bold magenta]mkdocs_puml[/bold magenta]: " + built_msg + ok_msg
