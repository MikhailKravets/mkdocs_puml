from unittest.mock import patch, MagicMock
from mkdocs_puml.puml import Fallback, PlantUML
from tests.conftest import BASE_PUML_URL


def test_url_with_slash():
    # Verify base_url ends with slash when provided with trailing slash
    puml = PlantUML(BASE_PUML_URL)
    assert puml.base_url.endswith("/")


def test_url_without_slash():
    # Ensure base_url ends with slash when provided without trailing slash
    puml = PlantUML(BASE_PUML_URL[:-1])
    assert puml.base_url.endswith("/")


def test_verify_ssl_default_enabled():
    # Verify SSL verification is enabled by default (using certifi CA bundle)
    puml = PlantUML(BASE_PUML_URL)
    assert puml.verify is True


def test_verify_ssl_disabled():
    # Verify SSL verification is disabled when set to false
    puml = PlantUML(BASE_PUML_URL, verify_ssl=False)
    assert puml.verify is False


def test_verify_ssl_system_certificates():
    # When verify_ssl is set to "system", verify should be an SSL context
    with patch('ssl.create_default_context') as mock_create_context:
        mock_context = MagicMock()
        mock_create_context.return_value = mock_context
        
        puml = PlantUML(BASE_PUML_URL, verify_ssl="system")
        
        mock_create_context.assert_called_once()
        mock_context.load_default_certs.assert_called_once()
        assert puml.verify == mock_context


def test_translate(diagram_and_encoded: tuple[str, str], mock_requests):
    # Verify translation of multiple diagrams to SVG
    diagram, encoded = diagram_and_encoded

    diagrams = [diagram] * 2

    mock_requests(len(diagrams))

    puml = PlantUML(BASE_PUML_URL)
    resp = puml.translate(diagrams)

    assert puml.base_url == f"{BASE_PUML_URL}svg/"

    assert len(resp) == 2

    for r in resp:
        assert r.startswith("<svg")
        assert not puml._html_comment_regex.search(r)
        assert 'preserveAspectRatio="xMidYMid meet"' in r


def test_translate_fallback(diagram_and_encoded: tuple[str, str], mock_requests_fallback):
    # Verify translation of multiple diagrams to SVG
    diagram, encoded = diagram_and_encoded

    diagrams = [diagram] * 2

    mock_requests_fallback(len(diagrams))

    puml = PlantUML(BASE_PUML_URL)
    resp = puml.translate(diagrams)

    assert len(resp) == 2

    for r in resp:
        assert isinstance(r, Fallback)
        assert r.status_code == 509
