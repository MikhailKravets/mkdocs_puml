from abc import ABC, abstractmethod
from typing import Iterable
import uuid

from mkdocs_puml.configs import CacheBackend, CacheConfig
from mkdocs_puml.diagrams import Diagram, ThemeMode


class AbstractStorage(ABC):
    def __init__(self):
        self.data: dict[str, Diagram] = {}

    def add(self, d: Diagram, replace: bool = False) -> str:
        h = self.hash(d)

        if replace:
            self.data[h] = d
            return h

        if h not in self.data:
            self.data[h] = d

        return h

    def update(self, d: Iterable[tuple[str, str]]):
        for key, svg in d:
            self.data[key].diagram = svg

    @abstractmethod
    def hash(self, d: Diagram) -> str:
        pass

    @abstractmethod
    def save(self):
        pass

    @property
    def schemes(self) -> Iterable[str]:
        return (v.scheme for v in self.data.values() if v.diagram is None)

    @property
    def iter_svg(self) -> Iterable[str]:
        return (v.diagram for v in self.data.values())

    @property
    def diagrams(self) -> Iterable[Diagram]:
        return self.data.values()

    @property
    def keys(self) -> Iterable[str]:
        return self.data.keys()

    def __getitem__(self, key: str) -> Diagram:
        return self.data[key]


class NaiveStorage(AbstractStorage):

    def hash(self, d: Diagram):
        if d.mode == ThemeMode.LIGHT:
            return str(uuid.uuid4())
        elif d.mode == ThemeMode.DARK:
            return f"{uuid.uuid4()}-dark"

    def save(self):
        """NaiveStorage keeps diagrams in RAM only"""


class FileStorage(AbstractStorage):
    pass


def build_storage(config: CacheConfig) -> AbstractStorage:
    if config.backend == CacheBackend.DISABLED.value:
        return NaiveStorage()
    elif config.backend == CacheBackend.LOCAL.value:
        return FileStorage()
