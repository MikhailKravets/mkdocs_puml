# Kanagawa :ocean:

<img src="/assets/themes/kanagawa/kanagawa%402x.png" width=300 />

-----------------

Kanagawa theme implements a color palette defined in [kanagawa.nvim](https://github.com/rebelot/kanagawa.nvim).
This color scheme is inspired by Katsushika Hokusai’s work, especially, his famous "The Great Wave".

## How to use

In order to use this theme with `mkdocs_puml`, set `theme` config of the plugin as follows:

```yaml
plantuml:
  theme:
    light: kanagawa/fuji
    dark: kanagawa/wave
```

## Flavors

This theme has two flavors

- `fuji` for light mode
- `wave` for dark mode

## Examples

Below you may find a few examples showing how this theme looks like.

### Class Diagram

=== "kanagawa/fuji"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/fuji.puml
    ' skinparam backgroundcolor white

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

=== "kanagawa/wave"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/wave.puml

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

=== "kanagawa/fuji"

    ```plantuml
    @startuml
    ' Substitute the link on desired theme
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/fuji.puml

    ' skinparam backgroundcolor white

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

=== "kanagawa/wave"

    ```plantuml
    @startuml
    ' Substitute the link on desired theme
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/wave.puml

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

=== "kanagawa/fuji"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/fuji.puml
    ' skinparam backgroundcolor white

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

=== "kanagawa/wave"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/wave.puml
    ' skinparam backgroundcolor white

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

=== "kanagawa/fuji"

    ```plantuml
    @startuml
    ' Substitute the link on desired theme
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/fuji.puml

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

=== "kanagawa/wave"

    ```plantuml
    @startuml
    ' Substitute the link on desired theme
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/wave.puml

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

=== "kanagawa/fuji"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/fuji.puml

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

=== "kanagawa/wave"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/wave.puml

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

=== "kanagawa/fuji"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/fuji.puml

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

=== "kanagawa/wave"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/kanagawa/wave.puml

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
