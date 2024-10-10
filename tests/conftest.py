from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock


BASE_PUML_URL = "http://mocked/"
BASE_PUML_KEYWORD = "puml"
CUSTOM_PUML_KEYWORD = "plantuml"
TESTDATA_DIR = Path(__file__).resolve().parent.joinpath("testdata")


@pytest.fixture(scope="package")
def diagram_and_encoded():
    """The fixture to return puml diagram and
    the encoded by plantuml.com string
    """
    return (
        "@startuml\nBob -> Alice : hello\n@enduml",
        "SoWkIImgAStDuNBAJrBGjLDmpCbCJbMmKiX8pSd9vt98pKi1IW80",
    )


@pytest.fixture(scope="package")
def c4_diagram():
    return """
    @startuml
    !include https://raw.git.../C4-PlantUML/master/C4_Container.puml
    System(test, "Test", "Test system")
    @enduml
    """


@pytest.fixture(scope="package")
def svg_diagram():
    with open(TESTDATA_DIR.joinpath("plantuml.svg")) as f:
        return f.read()


@pytest.fixture
def mock_requests(httpx_mock: HTTPXMock, svg_diagram):
    def expect(call_count: int):
        for _ in range(call_count):
            httpx_mock.add_response(content=svg_diagram.encode("utf-8"))
    return expect
