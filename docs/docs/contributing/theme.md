# Contribute Theme

We welcome contributions from theme creators to this project!
Whether you have a creative idea or want to implement a popular color
palette for PlantUML, we encourage you to get involved and share your
work with the community.
Follow the guide below to add your theme or update existing one in the repository.

## Structuring a theme

Each new theme should be placed in a folder named after the theme. The final `.puml`
file represents the theme flavor. So, showing what's being said, the theme structure should look like

```
theme_name/
  light_flavor.puml
  dark_flavor.puml
  dimmed_flavor.puml
  ...
```

## Work on theme

We encourage you to use a new styling API of PlantUML. You may read about styling API
at [Style (or CSS like style)](https://plantuml.com/en/style-evolution).
Although many features of the styling API are still in progress, it is a powerful mechanism for theming.
You may use themes from [Themes Hub](../themes/index.md) as a base when styling.

### Publishing your theme

Once you have prepared the theme flavors, please complete the theme card
in the project documentation `docs/themes/<theme-name>.md`. Usually, you'll want to include
the next topics to the theme card

- Theme name, logo, and short description;
- Color scheme used to create theme;
- Diagram examples using each flavor of the theme.

After that update [Themes Hub](../themes/index.md) available themes table.

Now, you're ready to create a PR on the `themes` branch and...

🙌 Thank you for your contribution!
