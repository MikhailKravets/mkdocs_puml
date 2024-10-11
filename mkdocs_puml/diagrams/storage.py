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

    def save(self):
        """NaiveStorage keeps diagrams in RAM only"""


class FileStorage(AbstractStorage):

    def __init__(self, base_dir: Path, filename: str = "storage.mpack"):
        super().__init__()

        work_dir = Path.cwd().name
        dir = base_dir.expanduser() / work_dir
        dir.mkdir(parents=True, exist_ok=True)

        self.path = dir / filename
        print(self.path)
        self._read_data()

    def hash(self, d: Diagram):
        return hashlib.blake2b(d.scheme.encode("utf-8")).hexdigest()

    # TODO: how to invalidate data?
    def save(self):
        with open(self.path, "wb") as f:
            msgpack.dump({k: dataclasses.asdict(v) for k, v in self.data.items()}, f)
        print("saved")

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
