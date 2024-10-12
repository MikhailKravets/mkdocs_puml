![logo](../.docs/logo_themes.svg)

## Themes available

|    **Name**      |    **Flavors**     |  **Light** | **Dark** | **C4** |  **Card**  |
|:----------:|:--------------:|:-----:|:-----:|:------:|:-----------------------:|
|    `default`     | <ul><li>`light`</li><li>`dark`</li></ul> | ✅ | ✅ | ✅ | [**themes/default**](default/README.md) |
| `catppuccin` | <ul><li>`latte`</li><li>`latte-white`</li><li>`frappe`</li><li>`macchiato`</li><li>`mocha`</li></ul> | ✅ | ✅ | ✅ | [**themes/catppuccin**](catppuccin/README.md)|

## How to use themes with mkdocs_puml

In order to configure themes you should add `theme` config as follows

```yml
theme:
  light: default/light
  dark: default/dark
```

- `light` specifies the theme to display on light mode
- `dark` specifies the theme to display on dark mode

Typically, a single theme has several flavors, allowing you to set the corresponding theme for each mode. For example, `default` theme has two flavors: `light` and `dark`.

### Using a custom themes repository

By default `mkdocs_puml` uses themes from its GitHub repository. However, if you like
to use your own themes, you should set `url` attribute and themes from that url

```yml
theme:
  url: https://your.custom.puml/themes
  light: custom/light
  dark: custom/dark
```

`mkdocs_puml` then builds a special URLs to access themes that follows this format

```
{url}/{mode}.puml
```

For our example above, `mkdocs_puml` will include into PlantUML diagrams these URLs

- Light mode `https://your.custom.puml/themes/custom/light.puml`
- Dark mode `https://your.custom.puml/themes/custom/dark.puml`

## Contribute theme

We welcome theme contributors to this project! Whether you have a creative idea
or want to implement a popular color palette for PlantUML,
we encourage you to get involved and share your work with the community.
Follow the guide below to add your theme or update existing one in the repository.

**TODO**: write guide.
