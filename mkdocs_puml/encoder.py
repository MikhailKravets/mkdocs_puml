import base64
import string
from zlib import compress

__all__ = ("encode",)

_B64_CHARS = f"{string.ascii_uppercase}{string.ascii_lowercase}{string.digits}+/"
_PUML_CHARS = f"{string.digits}{string.ascii_uppercase}{string.ascii_lowercase}-_"

_TRANSLATE_MAP = bytes.maketrans(_B64_CHARS.encode("utf-8"), _PUML_CHARS.encode("utf-8"))


def encode(content: str) -> str:
    """Encode plantUML diagram into a string
    that can be used in a communication with
    plantUML service.

    Read more at https://plantuml.com/en/text-encoding

    Args:
        content (str): plantUML diagram in a string representation

    Returns:
        Encoded string that can be used in plantUML service
        to build diagram images
    """
    content = compress(content.encode("utf-8"))[2:-4]  # 0:2 - header, -4: - checksum
    content = base64.b64encode(content)
    content = content.translate(_TRANSLATE_MAP)
    return content.decode("utf-8")
