from pathlib import Path
import typing
import re
import uuid
import os
import shutil

from mkdocs.config.base import Config
from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin

from mkdocs_puml.puml import PlantUML


class PlantUMLPlugin(BasePlugin):
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

    pre_class_name = "diagram-uuid"

    config_scheme = (
        ("puml_url", Type(str, required=True)),
        ("num_workers", Type(int, default=8)),
        ("puml_keyword", Type(str, default="puml")),
        ("verify_ssl", Type(bool, default=True)),
        ("auto_dark", Type(bool, default=True)),
    )

    def __init__(self):
        self.regex: typing.Optional[typing.Any] = None
        self.uuid_regex = re.compile(
            rf'<pre class="{self.pre_class_name}">(.+?)</pre>', flags=re.DOTALL
        )

        self.puml: typing.Optional[PlantUML] = None
        self.diagrams = {
            # key - uuid: value - puml. After on_env — svg
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
        config['extra_css'].append("assets/stylesheets/puml.css")
        self.puml_light = PlantUML(
            self.config["puml_url"],
            num_workers=self.config["num_workers"],
            verify_ssl=self.config["verify_ssl"],
            output_format="svg",
        )
        self.puml_dark = PlantUML(
            self.config["puml_url"],
            num_workers=self.config["num_workers"],
            verify_ssl=self.config["verify_ssl"],
            output_format="dsvg",
        )
        self.puml_keyword = self.config["puml_keyword"]
        self.regex = re.compile(rf"```{self.puml_keyword}(\n.+?)```", flags=re.DOTALL)
        self.auto_dark = self.config["auto_dark"]
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
            id_ = str(uuid.uuid4())
            self.diagrams[id_] = v
            markdown = markdown.replace(
                f"```{self.puml_keyword}{v}```", f'<pre class="{self.pre_class_name}">{id_}</pre>'
            )

        return markdown

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
        # TODO: self.diagrams changes its structure throughout a program run:
        #       1. Initially it's {key: "value"}
        #       2. After translate, it's {key: ("light_svg", "dark_svg" | None)}
        #       3. Align to a single format
        diagram_contents = [diagram for diagram in self.diagrams.values()]

        if self.auto_dark:
            light_svgs = self.puml_light.translate(diagram_contents)
            dark_svgs = self.puml_dark.translate(diagram_contents)
            for key, light_svg, dark_svg in zip(self.diagrams, light_svgs, dark_svgs):
                self.diagrams[key] = (light_svg, dark_svg)
        else:
            svgs = self.puml_light.translate(diagram_contents)
            for key, svg in zip(self.diagrams, svgs):
                self.diagrams[key] = (svg, None)
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
        light_svg, dark_svg = self.diagrams[key]
        if dark_svg:
            replacement = (
                f'<div class="puml light">{light_svg}</div>'
                f'<div class="puml dark">{dark_svg}</div>'
            )
        else:
            replacement = f'<div class="puml light">{light_svg}</div>'
        return content.replace(f'<pre class="{self.pre_class_name}">{key}</pre>', replacement)

    def on_post_build(self, config):
        """
        Event triggered after the build process is complete.

        This method is responsible for copying static files from the plugin's
        `static` directory to the specified `assets/javascripts/puml` directory
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
