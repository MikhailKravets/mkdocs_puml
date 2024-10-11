import pytest
from mkdocs_puml.model import Diagram, ThemeMode
from mkdocs_puml.storage import RAMStorage
from tests.plugins.conftest import is_uuid_valid


@pytest.fixture
def diagram_object():
    return Diagram("test", ThemeMode.LIGHT, "test")


def test_hash_light(diagram_object):
    storage = RAMStorage()
    assert is_uuid_valid(storage.hash(diagram_object))


def test_hash_dark(diagram_object):
    diagram_object.mode = ThemeMode.DARK
    storage = RAMStorage()

    h, _, dark = storage.hash(diagram_object).rpartition("-")
    assert is_uuid_valid(h)
    assert dark == "dark"


def test_add(diagram_object):
    storage = RAMStorage()
    key = storage.add(diagram_object)

    assert is_uuid_valid(key)
    assert len(storage.items()) == 1

    assert storage.items()[0][1] == diagram_object
