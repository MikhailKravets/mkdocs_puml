# Configuration

Only the `puml_url` parameter is required.
For the rest of parameters `mkdocs_puml` uses default values.
However you may modify the behavior of the plugin as needed.

??? info "In a hurry? Check out the complete table of parameters"

    | Parameter      | Type                   | Description                                                                 |
    |----------------|------------------------|-----------------------------------------------------------------------------|
    | `puml_url`     | `str`. Required        | URL to the PlantUML service                                                 |
    | `puml_keyword` | `str`. Default `puml`  | The keyword for PlantUML code fence, i.e. \```puml \```                     |
    | `verify_ssl`   | `bool`. Default `True` | Designates whether `requests` should verify SSL or not                      |
    | `verbose`      | `bool`. Default `True` | Designates whether `mkdocs_puml` should print status messages to console    |
    | `theme.enabled` | `bool`. Default `True` | Designates whether `plantuml` plugin should manage themes of the diagrams |
    | `theme.light`  | `str`. Default `default/light` | Name of the theme to use when `mkdocs-material` is in light mode |
    | `theme.dark`  | `str`. Default `default/dark` | Name of the theme to use when `mkdocs-material` is in dark mode |
    | `theme.url`   | `str`. Defaults to this [mkdocs_puml](https://github.com/MikhailKravets/mkdocs_puml) repository URL | URL to the repository folder where themes are located |
    | `cache.backend` | `enum`. `disabled` or `local` | Specifies the storage to use for preserving diagrams |
    | `cache.local.path` | `str`. Defaults to `~/.cache/mkdocs_puml` | Defines path where `mkdocs_puml` stores diagrams |
    | `interaction.enabled` | `bool`. Defaults to `True` | Designates whether rendered diagrams should be interactive |

## PlantUML

Configure PlantUML

## Theming

## Cache

## Interaction
