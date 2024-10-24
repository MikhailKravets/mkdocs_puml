from enum import Enum
from mkdocs.config.base import Config
from mkdocs.config.config_options import Type, SubConfig, Choice


class CacheBackend(Enum):
    DISABLED = "disabled"
    LOCAL = "local"

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class ThemeConfig(Config):
    enabled = Type(bool, default=True)
    light = Type(str, default="default/light")
    dark = Type(str, default="default/dark")

    url = Type(
        str,
        default="https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/master/themes/",
    )


class LocalCacheConfig(Config):
    path = Type(str, default="~/.cache/mkdocs_puml/")
    join_project_name = Type(bool, default=True)


class CacheConfig(Config):
    backend = Choice(CacheBackend.values(), default=CacheBackend.LOCAL.value)
    local = SubConfig(LocalCacheConfig)


class InteractionConfig(Config):
    enabled = Type(bool, default=True)


class PlantUMLConfig(Config):
    puml_url = Type(str)
    puml_keyword = Type(str, default="puml")
    verify_ssl = Type(bool, default=True)
    verbose = Type(bool, default=True)
    request_timeout = Type(int, default=300)
    theme = SubConfig(ThemeConfig)  # SubConfig already has an `{}` as default
    cache = SubConfig(CacheConfig)
    interaction = SubConfig(InteractionConfig)
