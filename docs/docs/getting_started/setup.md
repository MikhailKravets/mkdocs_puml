# Setup

`mkdocs_puml` allows you to modify its behavior with a set of parameters.

??? note "In a hurry? Take a look at the complete configuration"

    ```yaml
    plugins:
    - plantuml:
        puml_url: https://www.plantuml.com/plantuml/
        puml_keyword: puml
        request_timeout: 300
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
            join_project_name: true
        interaction:
          enabled: true
    ```

## PlantUML

The communication of `mkdocs_puml` with PlantUML server can be configured with these settings.

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

### `request_timeout`

Designates how much time in seconds `mkdocs_puml` will wait for a response from PlantUML server.
Defaults to 300 seconds. Set as

```yaml
plugins:
  - plantuml:
      request_timeout: 300
```

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

## Theming <theming>

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

By default `mkdocs_puml` attaches to its own [Themes Hub](../themes/index.md)
and uses [Default](../themes/default.md) PlantUML theme.

To set a theme, you should set a theme for each mode light and dark

```yaml
plugins:
  - plantuml:
      theme:
        light: catppuccin/frappe
        dark: catppuccin/mocha
```

??? note "What theme uses this documentation web-site?"

    This documentation web-site uses [Material](../themes/material.md) theme
    with the following setup

    ```yaml
    plugins:
    - plantuml:
        theme:
          light: material/teal-light
          dark: material/deep-orange-dark
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
as follows

```
@startuml

!include https://your.path/to/custom/themes/custom/light.puml
```

## Cache <cache>

The `mkdocs_puml` plugin implements a concept of storage that is used as a cache.
The plugin doesn't rebuild the diagrams that haven't changed, instead it loads
them from a storage.

You can manage the behavior of caching using `cache` parameter. By default
the plugin stores diagrams locally at `~/.cache/mkdocs_puml`. This cache
backend has a name `local` and it's the only available backend right now.
You can configure the `path` in which `mkdocs_puml` stores the diagrams
as follows

```yaml
plugins:
  plantuml:
    cache:
      backend: local
      local:
        path: "~/.cache/mkdocs_puml"
```

???+ note "Multiple Projects"

    The plugin creates its own caching directory for each project.
    So you can safely work on multiple `mkdocs` projects at the same time.

### `join_project_name`

By default, the local cache expects all cached files to be stored in a single directory.
To support multiple projects, it appends the project name (the name of the current working directory)
to the cache file path. This ensures that each project's cache is kept separate.

You can disable joining of project name by passing `false` to `join_project_name` as follows

```yaml
plugins:
  plantuml:
    cache:
      backend: local
      local:
        join_project_name: false
```

???+ tip "Using `mkdocs_puml` with CI tool"

    Often, PlantUML code includes a lot of URLs pointing to GitHub resources.
    That may result in rate limit errors, forcing you to build your documentation
    several times. This is especially problematic when building the documentation
    using CI tool.

    You can set a cache `path` to the relative directory inside your repository resulting in
    a config similar to

    ```yaml
    plugins:
      plantuml:
        cache:
          backend: local
          local:
            path: "diagrams"
            join_project_name: false
    ```

    `mkdocs_puml` will keep the diagrams in `${cwd}/diagrams/storage.mpack` file.

    You can then commit the diagrams file to the Git and use it in CI process.

Under the hood, local storage saves diagrams in [Message Pack](https://msgpack.org/) format.

To disable caching and rebuild all diagrams with every documentation change, use
the following configuration

```yaml
plugins:
  plantuml:
    cache:
      backend: disabled
```

## Interaction

Interaction settings control how users can interact with the rendered diagram.
Currently, you may either enable or disable the interaction as follows

```yaml
plugins:
  plantuml:
    interaction:
      enabled: true
```

???+ warning "Experimental Feature"

    At this time, interaction with the diagrams is an experimental feature
    and may not work as expected.
