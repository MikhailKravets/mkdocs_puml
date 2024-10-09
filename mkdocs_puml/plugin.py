from dataclasses import dataclass
from pathlib import Path
import typing
import re
import uuid
import os
import shutil

from mkdocs.config.base import Config
from mkdocs.config.config_options import Type, SubConfig, Optional
from mkdocs.plugins import BasePlugin

from mkdocs_puml.puml import PlantUML
from mkdocs_puml.themes import Theme


class ThemeConfig(Config):
    enabled = Type(bool, default=True)
    light = Type(str, default="default/light")
    dark = Type(str, default="default/dark")
    url = Type(
        str,
        default="https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/feature/themes/themes/",
    )


class PlantUMLConfig(Config):
    puml_url = Type(str)
    num_workers = Type(int, default=8)
    puml_keyword = Type(str, default="puml")
    verify_ssl = Type(bool, default=True)
    auto_dark = Type(  # TODO: deprecate! And we can set 1.5.0 version?
        bool, default=True
    )
    theme = SubConfig(ThemeConfig)  # SubConfig already has an `{}` as default


class ThemeMode:
    LIGHT = "light"
    DARK = "dark"


@dataclass
class Diagram:
    scheme: str
    mode: ThemeMode
    diagram: Optional[str] = None


class PlantUMLPlugin(BasePlugin[PlantUMLConfig]):
    """MKDocs plugin that converts puml diagrams into SVG images.

    It works only with a remote PlantUML service. You should add
    these configs into ``mkdocs.yml``::

            plugins:
                - mkdocs_puml:
                    puml_url: https://www.plantuml.com/plantuml
                    num_workers: 10

    Attributes:
        pre_class_name (str): the class that will be set to intermediate <pre> tag
                              containing uuid code
        config_scheme (str): config scheme to set by user in mkdocs.yml file

        regex (re.Pattern): regex to find all puml code blocks
        uuid_regex (re.Pattern): regex to find all uuid <pre> blocks
        puml (PlantUML): PlantUML instance that requests PlantUML service
        diagrams (dict): Dictionary containing the diagrams (puml and later svg) and their keys
        puml_keyword (str): keyword used to find PlantUML blocks within Markdown files
        verify_ssl (bool): Designates whether the ``requests`` should verify SSL certificate
        auto_dark (bool): Designates whether the plugin should automatically generate dark mode images.
    """

    pre_class_name = "diagram-key"

    def __init__(self):
        self.regex: typing.Optional[typing.Any] = None
        self.uuid_regex = re.compile(
            rf'<pre class="{self.pre_class_name}">(.+?)</pre>', flags=re.DOTALL
        )

        self.puml: typing.Optional[PlantUML] = None

        self.diagrams: dict[str, Diagram] = {
            # key - uuid: value - Diagram dataclass.
        }

    def on_config(self, config: Config) -> Config:
        """Event that is fired by mkdocs when configs are created.

        self.puml_light, self.puml_dark instances are populated in this event.
        Also, `puml.css` that enable dark / light mode styles is added to `extra_css`.

        Args:
            config: Full mkdocs.yml config file. To access configs of PlantUMLPlugin only,
                    use self.config attribute.

        Returns:
            Full config of the mkdocs
        """
        config["extra_css"].append("assets/stylesheets/puml.css")

        self.puml = PlantUML(
            self.config["puml_url"],
            num_workers=self.config["num_workers"],
            verify_ssl=self.config["verify_ssl"],
        )
        self.puml_keyword = self.config["puml_keyword"]
        self.regex = re.compile(rf"```{self.puml_keyword}(\n.+?)```", flags=re.DOTALL)

        if self.config.theme.enabled:
            self.themer = Theme(self.config.theme.url)

            self.theme_light = self.config.theme.light
            self.theme_dark = self.config.theme.dark
        else:
            self.themer = None
            self.theme_light = None
            self.theme_dark = None

        return config

    def on_page_markdown(self, markdown: str, *args, **kwargs) -> str:
        """Event to fire for each .md page.

        Here, all ``puml`` code blocks are found and added to self.diagrams
        with the corresponding uuid key.

        Then, <pre class="...">{uuid of diagram}</pre> tags are added to
        the markdown page.

        Args:
            markdown: Markdown page in which to look for ``puml`` diagrams.

        Returns:
            Updated markdown page
        """
        schemes = self.regex.findall(markdown)

        for v in schemes:
            if self.themer:
                replace_into = self._store_dual(v)
            else:
                replace_into = self._store_single(v)
            markdown = markdown.replace(
                f"```{self.puml_keyword}{v}```",
                replace_into,
            )

        return markdown

    def _store_single(self, scheme: str) -> str:
        key = str(uuid.uuid4())
        self.diagrams[key] = Diagram(scheme, mode=ThemeMode.LIGHT)
        return f'<pre class="{self.pre_class_name}">{key}</pre>'

    def _store_dual(self, scheme: str) -> str:
        key = str(uuid.uuid4())
        key_dark = f"{key}-dark"
        self.diagrams[key] = Diagram(
            self.themer.include(self.config.theme.light, scheme), mode=ThemeMode.LIGHT
        )
        self.diagrams[key_dark] = Diagram(
            self.themer.include(self.config.theme.dark, scheme), mode=ThemeMode.DARK
        )

        return (
            f'<pre class="{self.pre_class_name}">{key}</pre>\n'
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
        # Why it was even added??
        # diagram_contents = [diagram for diagram in self.diagrams.values()]

        svgs = self.puml.translate((v.scheme for v in self.diagrams.values()))
        for key, svg in zip(self.diagrams, svgs):
            self.diagrams[key].diagram = svg
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

            # MkDocs >=1.4 doesn't have html attribute.
            # This is required for integration with mkdocs-print-page plugin.
            # TODO: Remove the support of older versions in future releases
            if hasattr(page, "html") and page.html is not None:
                page.html = output

        return output

    def _replace(self, key: str, content: str) -> str:
        """Replace a UUID key with a real diagram in a
        content
        """
        diagram = self.diagrams[key]

        # When theming is not enabled, user will manually manage themes in each diagram.
        # Also, only one version of diagram will be generated for each scheme, which
        # should be displayed always although light / dark mode of mkdocs-material.
        style = "display: block" if not self.config.theme.enabled else ""
        replacement = (
            f'<div class="puml {diagram.mode}" style="{style}">{diagram.diagram}</div>'
        )
        return content.replace(
            f'<pre class="{self.pre_class_name}">{key}</pre>', replacement
        )

    def on_post_build(self, config):
        """
        Event triggered after the build process is complete.

        This method is responsible for copying static files from the plugin's
        `static` directory to the specified `assets/stylesheets/puml` directory
        in the site output. This ensures that the necessary JavaScript files
        are available in the final site.

        Args:
            config (dict): The MkDocs configuration object.

        """
        # Path to the static directory in the plugin
        puml_css = Path(__file__).parent.joinpath("static/puml.css")
        # Destination directory in the site output
        dest_dir = Path(config["site_dir"]).joinpath("assets/stylesheets/")

        if not dest_dir.exists():
            os.makedirs(dest_dir)

        shutil.copy(puml_css, dest_dir)
