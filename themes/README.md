![logo](../.docs/logo_themes.svg)

## Themes available

|    **Name**      |    **Flavors**     |  **Light** | **Dark** | **C4** |  **Card**  |
|:----------:|:--------------:|:-----:|:-----:|:------:|:-----------------------:|
|    `default`     | <ul><li>`light`</li><li>`dark`</li></ul> | ✅ | ✅ | ✅ | [**themes/default**](default/README.md) |
| `catppuccin` | <ul><li>`latte`</li><li>`latte-white`</li><li>`frappe`</li><li>`macchiato`</li><li>`mocha`</li></ul> | ✅ | ✅ | ✅ | [**themes/catppuccin**](catppuccin/README.md)|

## How to use themes

To use a theme, select the desired flavor, locate its .puml file, and include the raw file in your PlantUML code

```
!include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/default/dark.puml
```

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

We welcome contributions from theme creators to this project!
Whether you have a creative idea or want to implement a popular color
palette for PlantUML, we encourage you to get involved and share your
work with the community.
Follow the guide below to add your theme or update existing one in the repository.

### Structuring a theme

Each new theme should be placed in a folder named after the theme. The final `.puml`
file represents the theme flavor. Each theme folder should include a `README.md`
file that describes the theme and provides examples of diagrams that use this theme.
Examples can be placed under `examples/` folder.

So, showing what's being said, the theme structure should look like

```
theme_name/
  examples/
  light_flavor.puml
  dark_flavor.puml
  dimmed_flavor.puml
  README.md
```

### Work on theme

We encourage you to use a new styling API of PlantUML. You may read about styling API
at [Style (or CSS like style)](https://plantuml.com/en/style-evolution).
Although many features of the styling API are still in progress, it is a powerful mechanism for theming. You may use [default](default) theme as a base theme when
styling.

### Publishing your theme

Once you have prepared the theme flavors, please complete the theme card
(its `README.md`) to explain the theme, provide examples of various diagrams that
utilize it, and update [Themes available](#themes-available) table.

Then, please create a PR on the `themes` branch.

🙌 Thank you for your contribution!
