![logo](https://mikhailkravets.github.io/mkdocs_puml/assets/logos/logo.svg)

<h3 align="center">

<a href="https://pypi.org/project/mkdocs_puml/" target="_blank"><img src="https://img.shields.io/pypi/v/mkdocs-puml?style=for-the-badge" /></a>
<a href="https://pypistats.org/packages/mkdocs-puml" target="_blank"><img src="https://img.shields.io/pypi/dm/mkdocs_puml?style=for-the-badge" /></a>
<br />
<a href="https://mikhailkravets.github.io/mkdocs_puml/" target="_blank"><img src="https://img.shields.io/badge/Documentation-gray?style=for-the-badge&color=9D3058"></a>
<a href="https://mikhailkravets.github.io/mkdocs_puml/themes/" target="_blank"><img src="https://img.shields.io/badge/Themes%20Hub-449C90?style=for-the-badge&" /></a>

</h3>

`mkdocs_puml` is a fast and simple package that brings plantuml diagrams to MkDocs
documentation.

## Quick Start

Run the following command to install the package

```shell
pip install mkdocs_puml
```

After that, add `plantuml` plugin into `plugins` section of your `mkdocs.yml` file,
in order to use PlantUML with MkDocs.

```yaml
plugins:
  - plantuml:
      puml_url: https://www.plantuml.com/plantuml/
```

Not include PlantUML code fences with `puml` keyword to your documentation, such as

~~~
```puml
@startuml
Bob -> Alice : hello
@enduml
```
~~~

That's it, `mkdocs_puml` will automatically build `SVG` diagrams from the code 🎉

For more information, please refer to the [**documentation**](https://mikhailkravets.github.io/mkdocs_puml/).

## License

This project is licensed under MIT license.
