# Configuration

Only the `puml_url` parameter is required.
For the rest of parameters `mkdocs_puml` uses default values.
However you may modify the behavior of the plugin as needed.

??? info "In a hurry? Take a look at the complete configuration"

    ```yaml
    plugins:
    - plantuml:
        puml_url: https://www.plantuml.com/plantuml/
        puml_keyword: puml
        verify_ssl: true
        verbose: true
        theme:
          enabled: true
          light: default/light
          dark: default/dark
          url: https://raw.githubusercontent.com/.../mkdocs_puml/.../themes/
        cache:
          backend: local
          local:
            path: "~/.cache/mkdocs_puml"
        interaction:
          enabled: true
    ```

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

`mkdocs_puml` supports automatic theme switching for light and dark mode. It seamlessly integrates
with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/).

???+ info "Single-themed mode"

    Automatic theme switching comes with a cost, as `mkdocs_puml` need to generate two versions of every
    diagram. At the same time, having [caching](#cache) feature enabled, this overhead is almost negligible.

If you want to disable automatic theming set `enabled` parameter to `false`

```yaml
plugins:
    - plantuml:
        theme:
        enabled: false
```

### Using the `mkdocs_puml` Theme Repository

By default `mkdocs_puml` attaches to its own **Themes Hub**  **TODO**: insert link!!
and uses **default** PlantUML theme **TODO**: insert link on theme card!!

To set a theme, you should set a theme for each mode light and dark

```yaml
plugins:
  - plantuml:
      theme:
        light: catppuccin/frappe
        dark: catppuccin/mocha
```

??? info "This web-site uses catppuccin"

    This documentation web-site uses catppuccin theme **TODO**: insert link!!
    with special `catppuccin/frappe-white` flavor for light mode and
    `catppuccin/mocha` for dark mode. Use this configuration to apply the same
    settings for your setup

    ```yaml
    plugins:
    - plantuml:
        theme:
          light: catppuccin/frappe-white
          dark: catppuccin/mocha
    ```

### Using Custom Theme Repository

You can use your custom theme repository. For this you should set `url` parameter to your own server
and select themes in this server such as

```yaml
plugins:
- plantuml:
    theme:
        url: https://your.path/to/custom/themes
        light: custom/light
        dark: custom/dark
```

During build `mkdocs_puml` uses your URL to build two `!include` statements for each mode.
It simply attaches theme name to the end of the URL adding `.puml` extension. For the
above example, `mkdocs_puml` will generate the next URLs:

- For light mode `https://your.path/to/custom/themes/custom/light.puml`
- For dark mode `https://your.path/to/custom/themes/custom/dark.puml`

Then the plugin attaches the appropriate `!include` statement at the top of the diagram

```
@startuml

!include https://your.path/to/custom/themes/custom/light.puml
```

## Cache <cache>

## Interaction
