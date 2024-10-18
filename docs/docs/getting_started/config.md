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

You can manage PlantUML server behavior with these settings.

### `puml_url`

`puml_url` is the only required parameter that expects a URL to PlantUML server.
The easiest solution is to set URL to [plantuml.com/plantuml](https://www.plantuml.com/plantuml/) such as

```yaml
plugins:
  - plantuml:
      puml_url: https://www.plantuml.com/plantuml/
```

However, this approach has its disadvantages. First of all, you may not want to share private information
with the public server. Also, the public server has a rate limits, which can result in 509 errors.

As mentioned in [Installation](index.md#installation) section, you may setup PlantUML server locally
using Docker.

### `puml_keyword`

You can change the keyword that you'll use in code fences. For example,

```yaml
plugins:
  - plantuml:
      puml_keyword: uml
```

Then `mkdocs_puml` will search for the following blocks of code.

~~~
```uml
<your PUML code here>
```
~~~

### `verify_ssl`

In some cases, when using a custom PlantUML server setup, you may want to disable
SSL verification. This can be achieved by

```yaml
plugins:
  - plantuml:
      verify_ssl: false
```

By default `verify_ssl` is set to `true`.

???+ tip "Use self-signed SSL"

    Under the hood, `mkdocs_puml` uses [HTTPX](https://www.python-httpx.org/) to request PlantUML server.
    If you're running the server with self-signed certificates you need to set `SSL_CERT_FILE` or
    `SSL_CERT_DIR` environment variables before running `mkdocs`.

    For additional information refer to `HTTPX` documentation

    - [HTTPX - SSL](https://www.python-httpx.org/advanced/ssl/#making-https-requests-to-a-local-server).
    - [HTTPX - Environment Variables](https://www.python-httpx.org/environment_variables/#ssl_cert_dir).

### `verbose`

This parameter accepts boolean value and determines whether `mkdocs_puml` should display a status
message in the terminal. By default it is set to `true`. Use this config to disable this behavior

```yaml
plugins:
  - plantuml:
      verbose: false
```

## Theming

## Cache

## Interaction
