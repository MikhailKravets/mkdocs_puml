![logo](.docs/logo.png)

[![PyPI version](https://badge.fury.io/py/mkdocs_puml.svg)](https://badge.fury.io/py/mkdocs_puml)
[![PyPI Downloads](https://img.shields.io/pypi/dm/mkdocs_puml)](https://pypistats.org/packages/mkdocs-puml)

`mkdocs_puml` is a fast and simple package that brings plantuml diagrams to MkDocs
documentation.

## Install

Run the following command to install the package

```shell
pip install mkdocs_puml
```

## How to use

Just add `plantuml` plugin into `plugins` section of your `mkdocs.yml` file,
in order to use puml with mkdocs.

```yaml
plugins:
    - plantuml:
        puml_url: https://www.plantuml.com/plantuml/
```

`plantuml` plugin uses `PlantUML` only as an HTTP service. So, you should necessarily
specify `puml_url` config.

The `plantuml` config with the full list of parameters is below

```yaml
plugins:
    - plantuml:
        puml_url: https://www.plantuml.com/plantuml/
        num_workers: 8
        puml_keyword: puml
        verify_ssl: true
```

Where

| Parmeter | Type                 | Descripton                                                     |
|----------|----------------------|----------------------------------------------------------------|
| `puml_url` | `str`. Required      | URL to the plantuml service                                    |
| `num_workers` | `int`. Default `8`   | Max amount of concurrent workers that request plantuml service |
| `puml_keyword` | `str`. Default `puml` | The keyword for PlantUML code fence, i.e. \```puml \```        |
| `verify_ssl` | `bool`. Default `True` | Designates whether `requests` should verify SSL or not |

Now, you can put your puml diagrams into your `.md` documentation. For example,

<pre>
## PUML Diagram

```puml
@startuml
Bob -> Alice : hello
@enduml
```
</pre>

At the build step `mkdocs` sends requests to `puml_url` and substitutes your
diagram with the `svg` images from the responses.

### Run PlantUML service with Docker

It is possible to run [plantuml/plantuml-server](https://hub.docker.com/r/plantuml/plantuml-server)
as a Docker container.

Add a new service to the `docker-compose.yml` file

```yaml
version: "3"
services:
  puml:
    image: plantuml/plantuml-server
    ports:
      - '8080:8080'
```

Then substitute `puml_url` config with the local URL in the `mkdocs.yml` file

```yaml
plugins:
    - plantuml:
        puml_url: http://127.0.0.1:8080
        num_workers: 8
```

Obviously, this approach works faster than
using remote [plantuml.com](https://www.plantuml.com/plantuml/).

### Standalone usage

You can use `PlantUML` converter without `mkdocs`. Below is the example,

```python
from mkdocs_puml.puml import PlantUML

puml_url = "https://www.plantuml.com/plantuml"

diagram1 = """
@startuml
Bob -> Alice : hello
@enduml
"""

diagram2 = """
@startuml
Jon -> Sansa : hello
@enduml
"""

puml = PlantUML(puml_url, num_worker=2)
svg_for_diag1, svg_for_diag2 = puml.translate([diagram1, diagram2])
```

## How it works

The package uses PlantUML as an HTTP service. It sends GET requests to
PlantUML service and receives `svg` images representing the diagrams.

The `plantuml` plugin parses `.md` documentation files and looks for

<pre>
```puml

```
</pre>

code blocks. When `puml` code block is found it is saved to the buffer for
a later request to PlantUML service. In this step, we replace `puml` block
with the uuid.

**NOTE** you must set `puml` keyword as an indicator that the PlantUML diagram
is located in the block. Default keyword can be changed for the custom one
in `mkdocs.yml` config file by using `puml_keyword` parameter.

After all pages are parsed, `plantuml` plugin requests PlantUML service
with the collected diagrams. After the responses are received, the package
substitutes uuid codes in markdown files with the corresponding `svg` images.

## License

The project is licensed under [MIT license](LICENSE).

Diagram icon created by [Freepik](https://www.flaticon.com/free-icon/flow-chart_4411911?related_id=4411911&origin=search).
