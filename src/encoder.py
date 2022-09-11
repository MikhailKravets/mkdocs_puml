import base64
import string
from zlib import compress

__all__ = ('encode',)

_b64_chars = f"{string.ascii_uppercase}{string.ascii_lowercase}{string.digits}+/"
_puml_chars = f"{string.digits}{string.ascii_uppercase}{string.ascii_lowercase}-_"

_TRANSLATE_MAP = bytes.maketrans(
    _b64_chars.encode('utf-8'),
    _puml_chars.encode('utf-8')
)


def encode(content: str) -> str:
    content = compress(content.encode('utf-8'))[2:-4]  # 0:2 - header, -4: - checksum
    content = base64.b64encode(content)
    content = content.translate(_TRANSLATE_MAP)
    return content.decode('utf-8')
