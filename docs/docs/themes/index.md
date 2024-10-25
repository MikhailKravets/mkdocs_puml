# Themes Hub

![logo](../assets/logos/logo-themes.svg)

Themes Hub is a collection of themes specifically designed for PlantUML with
a seamless integration with `mkdocs_puml`.

## Available Themes

Currently the hub consists of the following themes.

|    **Name**      | **Light** | **Dark** | **C4** |
|:----------|:--------------:|:-----:|:-----:|
| [Default](default.md) |  :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [Catppuccin](catppuccin.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [Nord](nord.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [Kanagawa](kanagawa.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [Material :simple-materialformkdocs:](material.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |

## How to Use

???+ note "Using Themes from Hub with `mkdocs_puml`"

    Refer to the [Setup Theming Section](../getting_started/setup.md#theming) to learn how
    use themes with `mkdocs_puml`.

To use a theme from the hub, locate its corresponding `.puml` file containing the styles.
Each theme card includes a link to its folder in the GitHub repository.
Open the folder, select the desired flavor, get raw link to the file,
and build the `!include` statements to insert into your PlantUML code.

For example, for `catppuccin/mocha` flavor's `!include` statement is

```
!include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/mocha.puml
```

## License

Themes from the hub are licensed under MIT license.
