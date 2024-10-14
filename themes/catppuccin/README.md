<h3 align="center">
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" width="100" alt="Logo"/><br/>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
	Catppuccin
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
</h3>

-----------------

[Catppuccin](https://catppuccin.com/) color palette for PlantUML diagrams.

## How to use

In order to use this theme with `mkdocs_puml`, set `theme` config of the plugin as follows:

```yml
theme:
    light: catppuccin/latte
    dark: catppuccin/mocha
```

## Flavors

All four flavors of [catppuccin](https://catppuccin.com/) are implemented for PlantUML
and C4 extension.

> ❕ A special `latte-white` flavor has been added, setting the base color to
> `#ffffff` instead of catppuccino's `#eff1f5`. Some users may find it more
> appealing when used with light mode.

|**catppuccin/latte**|**catppuccin/frappe**|
|:-------:|:--------:|
|![latte](examples/classes/classes-latte.svg)|![frappe](examples/classes/classes-frappe.svg)|
|![macchiato](examples/classes/classes-macchiato.svg)|![mocha](examples/classes/classes-mocha.svg)|
|**catppuccin/macchiato**|**catppuccin/mocha**|

## Examples

Let's see how various diagrams look with this theme.

### Sequence

Simple sequence diagram looks as follows

|**catppuccin/latte**|**catppuccin/frappe**|
|:-------:|:--------:|
|![latte](examples/sequence/sequence-latte.svg)|![frappe](examples/sequence/sequence-frappe.svg)|
|![macchiato](examples/sequence/sequence-macchiato.svg)|![mocha](examples/sequence/sequence-mocha.svg)|
|**catppuccin/macchiato**|**catppuccin/mocha**|

Sequence diagram with groups, notes, and dividers looks

|**catppuccin/latte**|**catppuccin/frappe**|
|:-------:|:--------:|
|![latte](examples/sequence/sequence-full-latte.svg)|![frappe](examples/sequence/sequence-full-frappe.svg)|
|![macchiato](examples/sequence/sequence-full-macchiato.svg)|![mocha](examples/sequence/sequence-full-mocha.svg)|
|**catppuccin/macchiato**|**catppuccin/mocha**|

### Entities Diagram

|**catppuccin/latte**|**catppuccin/frappe**|
|:-------:|:--------:|
|![latte](examples/entities/entities-latte.svg)|![frappe](examples/entities/entities-frappe.svg)|
|![macchiato](examples/entities/entities-macchiato.svg)|![mocha](examples/entities/entities-mocha.svg)|
|**catppuccin/macchiato**|**catppuccin/mocha**|

### Timing

|**catppuccin/latte**|**catppuccin/frappe**|
|:-------:|:--------:|
|![latte](examples/timing/timing-latte.svg)|![frappe](examples/timing/timing-frappe.svg)|
|![macchiato](examples/timing/timing-macchiato.svg)|![mocha](examples/timing/timing-mocha.svg)|
|**catppuccin/macchiato**|**catppuccin/mocha**|

### C4

This theme also supports [C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML)
extension.

|**catppuccin/latte**|**catppuccin/frappe**|
|:-------:|:--------:|
|![latte](examples/c4/c4-latte.svg)|![frappe](examples/c4/c4-frappe.svg)|
|![macchiato](examples/c4/c4-macchiato.svg)|![mocha](examples/c4/c4-mocha.svg)|
|**catppuccin/macchiato**|**catppuccin/mocha**|
