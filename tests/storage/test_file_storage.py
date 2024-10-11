from unittest.mock import MagicMock

from mkdocs_puml.model import Diagram, ThemeMode
from mkdocs_puml.storage import FileStorage


def test_read_nonexistent_file(patch_path):
    patch_path.exists = MagicMock()
    patch_path.exists.return_value = False

    fs = FileStorage(patch_path, "test.mock")

    assert patch_path.exists.call_count == 1
    assert len(fs.data) == 0
    assert len(fs.invalid) == 0


def test_read_empty_file(patch_path):
    patch_path.stat = MagicMock()
    patch_path.stat.return_value = MagicMock()
    patch_path.stat.return_value.st_size = 0

    fs = FileStorage(patch_path, "test.mock")

    assert patch_path.stat.call_count == 1
    assert len(fs.data) == 0
    assert len(fs.invalid) == 0


def test_read(patch_path, patch_stream, hash_diagrams):
    fs = FileStorage(patch_path, "test.mock")

    assert len(fs.data) == len(fs.invalid) == len(hash_diagrams)

    for k, v in hash_diagrams.items():
        assert fs[k] == v
        assert k in fs.invalid


def test_add_new(patch_path, patch_stream, hash_diagrams):
    fs = FileStorage(patch_path, "test.mock")
    d = Diagram("test_new", ThemeMode.DARK, "test")
    fs.add(d)

    assert len(fs.data) == len(hash_diagrams) + 1
    assert len(fs.invalid) == len(hash_diagrams)


def test_add_existing(patch_path, patch_stream, hash_diagrams):
    fs = FileStorage(patch_path, "test.mock")

    diagram_list = list(hash_diagrams.items())
    fs.add(diagram_list[0][1])

    assert len(fs.data) == len(hash_diagrams)
    assert len(fs.invalid) == len(hash_diagrams) - 1

    assert diagram_list[0][0] not in fs.invalid


def test_save(patch_path, patch_stream, hash_diagrams):
    fs = FileStorage(patch_path, "test.mock")
    fs.save()

    assert patch_stream.return_value.write.call_count == 1
