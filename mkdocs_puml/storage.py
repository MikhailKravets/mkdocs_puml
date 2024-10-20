from abc import ABC, abstractmethod
import dataclasses
import hashlib
from pathlib import Path
from typing import Iterable
import typing
import uuid

import msgpack

from mkdocs_puml.config import CacheBackend, CacheConfig
from mkdocs_puml.model import Count, Diagram, ThemeMode
from mkdocs_puml.puml import Fallback


class AbstractStorage(ABC):
    """PlantUML may take up to several seconds to render
    a single diagram. Storage adds a persistence to the built SVG,
    allowing to use it as a cache for the diagrams.
    """

    def __init__(self):
        self.data: dict[str, Diagram] = {}

        # this is a set of keys that should not be saved
        # in the next save(..) iteration
        self.invalid: set[str] = set()

    @abstractmethod
    def add(self, d: Diagram) -> str:  # pragma: no cover
        """Add a diagram to the storage and return
        a key of the diagram.

        Args:
            d (Diagram): diagram object to add to the storage

        Returns:
            str: key of the diagram
        """

    def update(self, svg: Iterable[tuple[str, typing.Union[str, Fallback]]]):
        """Update a collection of diagrams from an
        iterable of SVG images.

        Args:
            svg (Iterable[tuple[str, str | Fallback]]): iterable of tuples `(diagram key, svg)`
        """
        for key, s in svg:
            if isinstance(s, Fallback):
                self.invalid.add(key)
            self.data[key].diagram = s

    @abstractmethod
    def hash(self, d: Diagram) -> str:  # pragma: no cover
        """Returns a collision-free hash for the diagram

        Args:
            d (Diagram): diagram object

        Returns:
            str: string hash of the diagram
        """

    @abstractmethod
    def save(self):  # pragma: no cover
        """Saves data to a persistent storage: a file,
        database, etc
        """

    def schemes(self) -> dict[str, str]:
        """A dictionary of diagrams that doesn't have SVG
        image rendered for them.

        Returns:
            dict[str, str]: dictionary where key is diagram key
                            and value is diagram scheme
        """
        return {k: v.scheme for k, v in self.data.items() if v.diagram is None}

    def items(self) -> list[str, Diagram]:
        """A list of (key, Dictionary) tuples"""
        return [(k, v) for k, v in self.data.items()]

    def keys(self) -> Iterable[str]:
        """Iterable of diagram keys"""
        return self.data.keys()

    def count(self, total: bool = False) -> Count:
        light, dark = 0, 0
        for v in self.data.values():
            if total:
                if v.mode == ThemeMode.LIGHT:
                    light += 1
                else:
                    dark += 1
            elif v.diagram is None:
                if v.mode == ThemeMode.LIGHT:
                    light += 1
                else:
                    dark += 1

        return Count(light, dark)

    def __getitem__(self, key: str) -> Diagram:
        """Get diagram by key"""
        return self.data[key]


class RAMStorage(AbstractStorage):
    """RAMStorage doesn't provide persistence.
    The diagrams are stored in memory only.

    It may be useful when user wants to disable caching.
    """

    def hash(self, d: Diagram):
        if d.mode == ThemeMode.LIGHT:
            return str(uuid.uuid4())
        elif d.mode == ThemeMode.DARK:
            return f"{uuid.uuid4()}-dark"

    def add(self, d: Diagram):
        h = self.hash(d)
        self.data[h] = d
        return h

    def save(self):  # pragma: no coverage
        """RAMStorage keeps diagrams in RAM only"""


class FileStorage(AbstractStorage):
    """`FileStorage` handles diagrams stored in a file
    using the MessagePack format.

    This class can be used as a cache, sending only diagrams
    without an SVG image to the PlantUML server.

    `FileStorage` uses `blake2b` as a hasher for diagrams.

    Args:
        base_dir (Path): the directory where `FileStorage` stores the file.
        filename (str): name of the file. Defaults to "storage.mpack".
        join_project_name (bool): if set to true, the storage will join current
                            working directory name to the storage path making
                            it possible to keep storage in one place and work
                            with multiple projects. Otherwise, storage will
                            keep the file with data in base_dir as passed
    """

    def __init__(
        self, base_dir: Path, filename: str = "storage.mpack", join_project_name: bool = True
    ):
        super().__init__()
        dir = base_dir.expanduser()

        if join_project_name:
            work_dir = Path.cwd().name
            dir = dir.joinpath(work_dir)

        dir.mkdir(parents=True, exist_ok=True)
        self.path = dir.joinpath(filename)

        self._read_data()

        # This attribute helps in finding invalid diagrams
        # that don't exists in docs anymore but present in storage.
        #
        # During the build self.data will be populated by call of
        # self.add method. If the key was never added through self.add
        # method, then this diagram doesn't exist anymore in the docs
        # and it can be safely deleted from storage.
        self.invalid = set(self.data.keys())

    def hash(self, d: Diagram):
        return hashlib.blake2b(d.scheme.encode("utf-8")).hexdigest()

    def add(self, d: Diagram):
        h = self.hash(d)

        if h in self.invalid:
            self.invalid.remove(h)

        if h not in self.data:
            self.data[h] = d

        return h

    def save(self):
        with open(self.path, "wb") as f:
            to_save = {}
            for k, v in self.data.items():
                if k not in self.invalid:
                    to_save[k] = dataclasses.asdict(v)
            msgpack.dump(to_save, f)

    def _read_data(self):
        if not self.path.exists() or self.path.stat().st_size == 0:
            return

        with open(self.path, "rb") as f:
            raw = msgpack.load(f)
            self.data = {k: Diagram(**v) for k, v in raw.items()}


def build_storage(config: CacheConfig) -> AbstractStorage:
    """Factory function that returns a storage class instance
    based on the `CacheConfig`.

    Cache backend:

    * `disabled` — build `RAMStorage` instance
    * `local` — build `FileStorage` instance
    """
    if config.backend == CacheBackend.DISABLED.value:
        return RAMStorage()
    elif config.backend == CacheBackend.LOCAL.value:
        return FileStorage(
            Path(config.local.path), join_project_name=config.local.join_project_name
        )
