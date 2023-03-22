from pathlib import Path
from unittest.mock import Mock

import pytest
import requests


BASE_PUML_URL = "https://mocked.org/"
BASE_PUML_KEYWORD = "puml"
CUSTOM_PUML_KEYWORD = "plantuml"
TESTDATA_DIR = Path(__file__).resolve().parent.joinpath('testdata')


@pytest.fixture(scope="package")
def diagram_and_encoded():
    """The fixture to return puml diagram and
    the encoded by plantuml.com string
    """
    return "@startuml\nBob -> Alice : hello\n@enduml", "SoWkIImgAStDuNBAJrBGjLDmpCbCJbMmKiX8pSd9vt98pKi1IW80"


@pytest.fixture(scope="package")
def svg_diagram():
    with open(TESTDATA_DIR.joinpath('plantuml.svg')) as f:
        return f.read()


@pytest.fixture(scope="function")
def mock_requests(monkeypatch, svg_diagram):
    p = Mock()
    p.return_value.content = svg_diagram.encode('utf-8')
    monkeypatch.setattr(requests, "get", p)
    yield p
