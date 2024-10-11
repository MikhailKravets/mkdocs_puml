from abc import ABC, abstractmethod
import dataclasses
import hashlib
from pathlib import Path
from typing import Iterable
import uuid

import msgpack

from mkdocs_puml.configs import CacheBackend, CacheConfig
from mkdocs_puml.model import Diagram, ThemeMode


class AbstractStorage(ABC):
    """PlantUML may take up to several seconds to render
    a single diagram. Storage adds a persistence to the built SVG,
    allowing to use it as a cache for the diagrams.
    """

    def __init__(self):
        self.data: dict[str, Diagram] = {}

    @abstractmethod
    def add(self, d: Diagram) -> str:  # pragma: no cover
        """Add a diagram to the storage and return
        a key of the diagram.

        Args:
            d (Diagram): diagram object to add to the storage

        Returns:
            str: key of the diagram
        """

    def update(self, svg: Iterable[tuple[str, str]]):
        """Update a collection of diagrams from an
        iterable of SVG images.

        Args:
            svg (Iterable[tuple[str, str]]): iterable of tuples `(diagram key, svg)`
        """
        for key, s in svg:
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
        filename (str, optional): name of the file. Defaults to "storage.mpack".
    """

    def __init__(self, base_dir: Path, filename: str = "storage.mpack"):
        super().__init__()

        work_dir = Path.cwd().name
        dir = base_dir.expanduser().joinpath(work_dir)
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
            msgpack.dump(
                {
                    k: dataclasses.asdict(v)
                    for k, v in self.data.items()
                    if k not in self.invalid
                },
                f,
            )

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
        return FileStorage(Path(config.local.path))
