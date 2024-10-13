from dataclasses import dataclass
from typing import Optional
import typing

from mkdocs_puml.puml import Fallback


class ThemeMode:
    LIGHT = "light"
    DARK = "dark"


@dataclass
class Diagram:
    scheme: str
    mode: ThemeMode
    diagram: Optional[typing.Union[str, Fallback]] = None


@dataclass
class Count:
    light: int
    dark: int
