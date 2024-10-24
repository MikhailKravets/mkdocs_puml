# Material

<img src="/assets/themes/material/mkdocs-material.svg" width=200 />

----------------

Meterial theme is a set of minimalistic flavors that implements
color palette of [mkdocs-material](https://squidfunk.github.io/mkdocs-material/).

[:material-github: Open Styles on GitHub](https://github.com/MikhailKravets/mkdocs_puml/tree/themes/themes/material){ .md-button }

## How to use

In order to use this theme with `mkdocs_puml`, select desired flavord and set `theme` config of the plugin as follows:

```yaml
plantuml:
  theme:
    light: material/indigo-light
    dark: material/indigo-dark
```

## Flavors

Material theme is flavors of all `mkdocs-material` primary colors listed below.

<button data-md-color-primary="red">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">red</code>
</button>
<button data-md-color-primary="pink">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">pink</code>
</button>
<button data-md-color-primary="purple">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">purple</code>
</button>
<button data-md-color-primary="deep-purple">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">deep purple</code>
</button>
<button data-md-color-primary="indigo">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">indigo</code>
</button>
<button data-md-color-primary="blue">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">blue</code>
</button>
<button data-md-color-primary="light-blue">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">light blue</code>
</button>
<button data-md-color-primary="cyan">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">cyan</code>
</button>
<button data-md-color-primary="teal">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">teal</code>
</button>
<button data-md-color-primary="green">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">green</code>
</button>
<button data-md-color-primary="light-green">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">light green</code>
</button>
<button data-md-color-primary="lime">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">lime</code>
</button>
<button data-md-color-primary="yellow">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">yellow</code>
</button>
<button data-md-color-primary="amber">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">amber</code>
</button>
<button data-md-color-primary="orange">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">orange</code>
</button>
<button data-md-color-primary="deep-orange">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">deep orange</code>
</button>
<button data-md-color-primary="brown">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">brown</code>
</button>
<button data-md-color-primary="grey">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">grey</code>
</button>
<button data-md-color-primary="blue-grey">
    <code style="background-color: var(--md-primary-fg-color); color: var(--md-primary-bg-color); border-radius: .1rem">blue grey</code>
</button>

So, it supports every color except `black` and `white`.

Each flavor is named after its primary color and implemented in two variants: `light` and `dark`.
Flavor name is structured as `{primary-color}-{mode}`. For instance, if we want to use `deep-purple` color counterpart,
we'll use `deep-purple-light` for light mode and `deep-purple-dark`.

The following tab-panel contains the `mkdocs_puml` configurations of all material flavors.

=== "red"

    ```yaml
    plantuml:
      theme:
        light: material/red-light
        dark: material/red-dark
    ```

=== "pink"

    ```yaml
    plantuml:
      theme:
        light: material/pink-light
        dark: material/pink-dark
    ```

=== "purple"

    ```yaml
    plantuml:
      theme:
        light: material/purple-light
        dark: material/purple-dark
    ```

=== "deep purple"

    ```yaml
    plantuml:
      theme:
        light: material/deep-purple-light
        dark: material/deep-purple-dark
    ```

=== "indigo"

    ```yaml
    plantuml:
      theme:
        light: material/indigo-light
        dark: material/indigo-dark
    ```

=== "blue"

    ```yaml
    plantuml:
      theme:
        light: material/blue-light
        dark: material/blue-dark
    ```

=== "purple"

    ```yaml
    plantuml:
      theme:
        light: material/light-blue-light
        dark: material/light-blue-dark
    ```

=== "cyan"

    ```yaml
    plantuml:
      theme:
        light: material/cyan-light
        dark: material/cyan-dark
    ```

=== "teal"

    ```yaml
    plantuml:
      theme:
        light: material/teal-light
        dark: material/teal-dark
    ```

=== "green"

    ```yaml
    plantuml:
      theme:
        light: material/green-light
        dark: material/green-dark
    ```

=== "light green"

    ```yaml
    plantuml:
      theme:
        light: material/light-green-light
        dark: material/light-green-dark
    ```

=== "lime"

    ```yaml
    plantuml:
      theme:
        light: material/lime-light
        dark: material/lime-dark
    ```

=== "yellow"

    ```yaml
    plantuml:
      theme:
        light: material/yellow-light
        dark: material/yellow-dark
    ```

=== "amber"

    ```yaml
    plantuml:
      theme:
        light: material/amber-light
        dark: material/amber-dark
    ```

=== "orange"

    ```yaml
    plantuml:
      theme:
        light: material/orange-light
        dark: material/orange-dark
    ```

=== "deep orange"

    ```yaml
    plantuml:
      theme:
        light: material/deep-orange-light
        dark: material/deep-orange-dark
    ```

=== "brown"

    ```yaml
    plantuml:
      theme:
        light: material/brown-light
        dark: material/brown-dark
    ```

=== "grey"

    ```yaml
    plantuml:
      theme:
        light: material/grey-light
        dark: material/grey-dark
    ```

=== "blue grey"

    ```yaml
    plantuml:
      theme:
        light: material/blue-grey-light
        dark: material/blue-grey-dark
    ```

## Examples

In this theme card, we'll showcase examples using the classic indigo flavor.
Feel free to experiment by trying out other flavors on your own.

### Class Diagram

=== "material/indigo-light"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-light.puml
    skinparam backgroundcolor white

    interface Display {
        Represent an object in String
    }

    abstract class AbstractReader {
        Read the data from various sources
        ..
        +read() -> Vec<Data>
    }

    enum Category {
        + DEVICE
        + FOOD
        + MISC
    }

    class Item {
        Object representing a data item
        ..
        +name: String
        +category: Category
        +price: f64
    }

    Item --* Category
    AbstractReader --o Item

    package fs {
        class CSVReader {
            Read data from csv file
            ..
            +new(p: AsRef<Path>) -> Self
            +read() -> Vec<Data>
        }

        class JSONReader {
            Read data from json file
            ..
            +new(p: AsRef<Path>) -> Self
            +read() -> Vec<Data>
        }
    }

    CSVReader -up-> AbstractReader
    JSONReader -up-> AbstractReader

    Category --> Display
    Item --> Display

    @enduml
    ```

=== "material/indigo-dark"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-dark.puml
    skinparam backgroundcolor #1e2129

    interface Display {
        Represent an object in String
    }

    abstract class AbstractReader {
        Read the data from various sources
        ..
        +read() -> Vec<Data>
    }

    enum Category {
        + DEVICE
        + FOOD
        + MISC
    }

    class Item {
        Object representing a data item
        ..
        +name: String
        +category: Category
        +price: f64
    }

    Item --* Category
    AbstractReader --o Item

    package fs {
        class CSVReader {
            Read data from csv file
            ..
            +new(p: AsRef<Path>) -> Self
            +read() -> Vec<Data>
        }

        class JSONReader {
            Read data from json file
            ..
            +new(p: AsRef<Path>) -> Self
            +read() -> Vec<Data>
        }
    }

    CSVReader -up-> AbstractReader
    JSONReader -up-> AbstractReader

    Category --> Display
    Item --> Display

    @enduml
    ```

### Sequence

=== "material/indigo-light"

    ```plantuml
    @startuml
    ' Substitute the link on desired theme
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-light.puml
    skinparam backgroundcolor white

    Alice -> Bob: Authentication Request

    == Initialization ==

    note left: this is a first note

    alt successful case

        Bob -> Alice: Authentication Accepted

    else some kind of failure

        Bob -> Alice: Authentication Failure
        Alice -> Log : Log attack start
        Alice -> Log : Log attack end

    else Another type of failure

    Bob -> Alice: Please repeat

    end
    @enduml
    ```

=== "material/indigo-dark"

    ```plantuml
    @startuml
    ' Substitute the link on desired theme
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-dark.puml
    skinparam backgroundcolor #1e2129

    Alice -> Bob: Authentication Request

    == Initialization ==

    note left: this is a first note

    alt successful case

        Bob -> Alice: Authentication Accepted

    else some kind of failure

        Bob -> Alice: Authentication Failure
        Alice -> Log : Log attack start
        Alice -> Log : Log attack end

    else Another type of failure

    Bob -> Alice: Please repeat

    end
    @enduml
    ```

### State

=== "material/indigo-light"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-light.puml
    skinparam backgroundcolor white

    scale 350 width
    [*] --> NotShooting

    state NotShooting {
    [*] --> Idle
    Idle --> Configuring : EvConfig
    Configuring --> Idle : EvConfig
    }

    state Configuring {
    [*] --> NewValueSelection
    NewValueSelection --> NewValuePreview : EvNewValue
    NewValuePreview --> NewValueSelection : EvNewValueRejected
    NewValuePreview --> NewValueSelection : EvNewValueSaved

    state NewValuePreview {
        State1 -> State2
    }

    }
    @enduml
    ```

=== "material/indigo-dark"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-dark.puml
    skinparam backgroundcolor #1e2129

    scale 350 width
    [*] --> NotShooting

    state NotShooting {
    [*] --> Idle
    Idle --> Configuring : EvConfig
    Configuring --> Idle : EvConfig
    }

    state Configuring {
    [*] --> NewValueSelection
    NewValueSelection --> NewValuePreview : EvNewValue
    NewValuePreview --> NewValueSelection : EvNewValueRejected
    NewValuePreview --> NewValueSelection : EvNewValueSaved

    state NewValuePreview {
        State1 -> State2
    }

    }
    @enduml
    ```

### Entity

=== "material/indigo-light"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-light.puml
    skinparam backgroundcolor white

    title "Database"

    skinparam linetype ortho

    package "authentication.models" as auth_models{
        entity User{
            *id: INT<PK>
            ..
            *email: VARCHAR<unique, case_insensitive>
            *password: VARCHAR<argon2>
            *is_staff: BOOLEAN
            *is_superuser: BOOLEAN
            *is_active: BOOLEAN
            *last_login_at: TIMESTAMP
            *created_at: TIMESTAMP
        }
    }

    package "projects.models" as projects{
        entity Project{
            * id: INT<PK>
            ..
            * user: INT<FK>
            * name: VARCHAR
            * last_updated_at: TIMESTAMP
            * created_at: TIMESTAMP
        }
        entity UML{
            * id: INT<PK>
            ..
            * project: INT<FK>
            * c4_type: ENUM
            * diagram: TEXT
        }
        UML }--|| Project
        Project }o--|| User
    }

    package "user_cards.models" as user_cards{
        entity Card{
            * id: INT<PK>
            ..
            * user: INT<FK>
            * stripe_token: VARCHAR
            name: VARCHAR
            last_numbers: VARCHAR(4)
            * created_at: TIMESTAMP
        }
        Card }o--|| User
    }

    package "user_devices.models" as user_devices{
        entity PhoneDevice{
            * id: INT<PK>
            ..
            * user: INT<FK, unique>
            * phone_number: VARCHAR<unique=True>
            * secret_key: VARCHAR
        }

        PhoneDevice |o--|| User
    }
    @enduml
    ```

=== "material/indigo-dark"

    ```plantuml
    @startuml
    ' Substitute the link on desired theme
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-dark.puml
    skinparam backgroundcolor #1e2129

    title "Database"

    skinparam linetype ortho

    package "authentication.models" as auth_models{
        entity User{
            *id: INT<PK>
            ..
            *email: VARCHAR<unique, case_insensitive>
            *password: VARCHAR<argon2>
            *is_staff: BOOLEAN
            *is_superuser: BOOLEAN
            *is_active: BOOLEAN
            *last_login_at: TIMESTAMP
            *created_at: TIMESTAMP
        }
    }

    package "projects.models" as projects{
        entity Project{
            * id: INT<PK>
            ..
            * user: INT<FK>
            * name: VARCHAR
            * last_updated_at: TIMESTAMP
            * created_at: TIMESTAMP
        }
        entity UML{
            * id: INT<PK>
            ..
            * project: INT<FK>
            * c4_type: ENUM
            * diagram: TEXT
        }
        UML }--|| Project
        Project }o--|| User
    }

    package "user_cards.models" as user_cards{
        entity Card{
            * id: INT<PK>
            ..
            * user: INT<FK>
            * stripe_token: VARCHAR
            name: VARCHAR
            last_numbers: VARCHAR(4)
            * created_at: TIMESTAMP
        }
        Card }o--|| User
    }

    package "user_devices.models" as user_devices{
        entity PhoneDevice{
            * id: INT<PK>
            ..
            * user: INT<FK, unique>
            * phone_number: VARCHAR<unique=True>
            * secret_key: VARCHAR
        }

        PhoneDevice |o--|| User
    }
    @enduml
    ```

### Activity

=== "material/indigo-light"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-light.puml
    skinparam backgroundcolor white

    skinparam backgroundcolor white
    start
    fork
    :action 1;
    fork again
    :action 2;
    fork again
    :action 3;
    fork again
    :action 4;
    end merge
    stop
    @enduml
    ```

=== "material/indigo-dark"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-dark.puml
    skinparam backgroundcolor #1e2129

    start
    fork
    :action 1;
    fork again
    :action 2;
    fork again
    :action 3;
    fork again
    :action 4;
    end merge
    stop
    @enduml
    ```

### C4

C4 styling is remained mostly intact. The only change is an improved visibility in dark mode.

=== "material/indigo-light"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-light.puml
    skinparam backgroundcolor white

    ' skinparam backgroundcolor white

    !define DEVICONS https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/master/devicons
    !define FONTAWESOME https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/master/font-awesome-5
    !include DEVICONS/angular.puml
    !include DEVICONS/java.puml
    !include DEVICONS/msql_server.puml
    !include DEVICONS/redis.puml
    !include FONTAWESOME/users.puml

    Person(user, "Customer", "People that need products", $sprite="users")
    Container(spa, "SPA", "angular", "The main interface that the customer interacts with", $sprite="angular")
    Container(api, "API", "java", "Handles all business logic", $sprite="java")

    Container_Boundary(db_boundary, "Databases"){
    ContainerDb(db, "Database", "Microsoft SQL", "Holds product, order and invoice information", $sprite="msql_server")
    ContainerDb(redis, "Cache & MB", "Redis", "Cache and simple message broker", $sprite="redis")
    }

    Rel_D(user, spa, "Uses")
    Rel_R(spa, api, "Uses")
    Rel_R(api, db, "Reads/Writes")
    @enduml
    ```

=== "material/indigo-dark"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/material/indigo-dark.puml
    skinparam backgroundcolor #1e2129

    ' skinparam backgroundcolor white

    !define DEVICONS https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/master/devicons
    !define FONTAWESOME https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/master/font-awesome-5
    !include DEVICONS/angular.puml
    !include DEVICONS/java.puml
    !include DEVICONS/msql_server.puml
    !include DEVICONS/redis.puml
    !include FONTAWESOME/users.puml

    Person(user, "Customer", "People that need products", $sprite="users")
    Container(spa, "SPA", "angular", "The main interface that the customer interacts with", $sprite="angular")
    Container(api, "API", "java", "Handles all business logic", $sprite="java")

    Container_Boundary(db_boundary, "Databases"){
    ContainerDb(db, "Database", "Microsoft SQL", "Holds product, order and invoice information", $sprite="msql_server")
    ContainerDb(redis, "Cache & MB", "Redis", "Cache and simple message broker", $sprite="redis")
    }

    Rel_D(user, spa, "Uses")
    Rel_R(spa, api, "Uses")
    Rel_R(api, db, "Reads/Writes")
    @enduml
    ```
