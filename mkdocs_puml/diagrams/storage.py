from abc import ABC, abstractmethod
import dataclasses
import hashlib
from pathlib import Path
from typing import Iterable
import uuid

import msgpack

from mkdocs_puml.configs import CacheBackend, CacheConfig
from mkdocs_puml.diagrams import Diagram, ThemeMode


class AbstractStorage(ABC):
    def __init__(self):
        self.data: dict[str, Diagram] = {}

    @abstractmethod
    def add(self, d: Diagram) -> str:
        pass

    def update(self, d: Iterable[tuple[str, str]]):
        for key, svg in d:
            self.data[key].diagram = svg

    @abstractmethod
    def hash(self, d: Diagram) -> str:
        pass

    @abstractmethod
    def save(self):
        pass

    def schemes(self) -> dict[str, str]:
        return {k: v.scheme for k, v in self.data.items() if v.diagram is None}

    def items(self) -> dict[str, Diagram]:
        return [(k, v) for k, v in self.data.items()]

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

    def add(self, d: Diagram):
        h = self.hash(d)

        if h not in self.data:
            self.data[h] = d

        return h

    def save(self):
        """NaiveStorage keeps diagrams in RAM only"""


class FileStorage(AbstractStorage):

    def __init__(self, base_dir: Path, filename: str = "storage.mpack"):
        super().__init__()

        work_dir = Path.cwd().name
        dir = base_dir.expanduser() / work_dir
        dir.mkdir(parents=True, exist_ok=True)

        self.path = dir / filename
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
    if config.backend == CacheBackend.DISABLED.value:
        return NaiveStorage()
    elif config.backend == CacheBackend.LOCAL.value:
        return FileStorage(Path(config.local.path))
