

class Theme:

    def __init__(self, url: str) -> None:
        self.url = url

    @classmethod
    def from_github(cls, theme: str, maintainer: str, branch: str = "master"):
        # TODO: is it ok to hardcode extension .puml??
        return cls(
            f"https://raw.githubusercontent.com/{maintainer}/mkdocs_puml/{branch}/themes/{theme}.puml"
        )

    def embed(self, diagram: str) -> str:
        diagram = diagram.strip()
        if diagram.startswith("@startuml"):
            head, _, tail = diagram.partition("\n")
        else:
            head, tail = None, diagram

        if head:
            return f"{head}\n{self.include_stmt}\n{tail}"
        return f"{self.include_stmt}\n{tail}"

    @property
    def include_stmt(self) -> str:
        return f"!include {self.url}"
