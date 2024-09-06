from mkdocs_puml.encoder import encode


def test_encode(diagram_and_encoded: tuple[str, str]):
    # Ensures the encoded output matches the expected result.
    diagram, expected = diagram_and_encoded
    encoded = encode(diagram)

    assert encoded == expected
