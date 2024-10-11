from dataclasses import dataclass
from typing import Optional


class ThemeMode:
    LIGHT = "light"
    DARK = "dark"


@dataclass
class Diagram:
    scheme: str
    mode: ThemeMode
    diagram: Optional[str] = None
