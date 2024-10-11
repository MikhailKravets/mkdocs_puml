from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mkdocs_puml.model import Diagram, ThemeMode
from mkdocs_puml.storage import FileStorage


# TODO: find a better way to mock Path.
@pytest.fixture
def patch_exist_stat(monkeypatch, patch_path_mkdir):
    stat = MagicMock()
    stat.return_value = MagicMock()
    stat.return_value.st_size = 2

    exists = MagicMock()
    exists.return_value = True
    monkeypatch.setattr("pathlib.Path.exists", exists)
    monkeypatch.setattr("pathlib.Path.stat", stat)


def test_read_nonexistent_file(monkeypatch, patch_path_mkdir):
    exists = MagicMock()
    exists.return_value = False

    monkeypatch.setattr("pathlib.Path.exists", exists)

    fs = FileStorage(Path("test"), "test.mock")

    assert exists.call_count == 1
    assert len(fs.data) == 0
    assert len(fs.invalid) == 0


def test_read_empty_file(monkeypatch, patch_path_mkdir):
    stat = MagicMock()
    stat.return_value = MagicMock()
    stat.return_value.st_size = 0

    exists = MagicMock()
    exists.return_value = True
    monkeypatch.setattr("pathlib.Path.exists", exists)
    monkeypatch.setattr("pathlib.Path.stat", stat)

    fs = FileStorage(Path("test"), "test.mock")

    assert stat.call_count == 1
    assert len(fs.data) == 0
    assert len(fs.invalid) == 0


def test_read(monkeypatch, patch_exist_stat, patch_stream, hash_diagrams):
    fs = FileStorage(Path("test"), "test.mock")

    assert len(fs.data) == len(fs.invalid) == len(hash_diagrams)

    for k, v in hash_diagrams.items():
        assert fs[k] == v
        assert k in fs.invalid


def test_add_new(patch_exist_stat, patch_stream, hash_diagrams):
    fs = FileStorage(Path("test"), "test.mock")
    d = Diagram("test_new", ThemeMode.DARK, "test")
    fs.add(d)

    assert len(fs.data) == len(hash_diagrams) + 1
    assert len(fs.invalid) == len(hash_diagrams)


def test_add_existing(patch_exist_stat, patch_stream, hash_diagrams):
    fs = FileStorage(Path("test"), "test.mock")

    diagram_list = list(hash_diagrams.items())
    fs.add(diagram_list[0][1])

    assert len(fs.data) == len(hash_diagrams)
    assert len(fs.invalid) == len(hash_diagrams) - 1

    assert diagram_list[0][0] not in fs.invalid


def test_save(patch_exist_stat, patch_stream, hash_diagrams):
    fs = FileStorage(Path("test"), "test.mock")
    fs.save()

    assert patch_stream.return_value.write.call_count == 1
