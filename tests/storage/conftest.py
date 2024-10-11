import dataclasses
import hashlib
from unittest.mock import MagicMock, mock_open

import msgpack
import pytest
from mkdocs_puml.diagrams.models import Diagram, ThemeMode


@pytest.fixture
def patch_path(monkeypatch):
    path_mock = MagicMock()
    path_mock.expanduser.return_value = path_mock
    path_mock.__truediv__.return_value = path_mock
    monkeypatch.setattr("pathlib.Path", path_mock)

    return path_mock


@pytest.fixture
def hash_diagrams():
    d = [
        Diagram("test_one", ThemeMode.LIGHT, "test"),
        Diagram("test_two", ThemeMode.DARK, "test"),
    ]

    return {hashlib.blake2b(v.scheme.encode("utf-8")).hexdigest(): v for v in d}


@pytest.fixture
def patch_stream(monkeypatch, hash_diagrams):
    encoded = msgpack.dumps(
        {k: dataclasses.asdict(v) for k, v in hash_diagrams.items()}
    )
    mock = mock_open(read_data=encoded)
    monkeypatch.setattr("builtins.open", mock)
    return mock
