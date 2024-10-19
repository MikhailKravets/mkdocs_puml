# Catppuccin

<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" width="100" alt="Logo"/>

-----------------

[Catppuccin](https://catppuccin.com/) color palette for PlantUML diagrams.

## How to use

In order to use this theme with `mkdocs_puml`, set `theme` config of the plugin as follows:

```yaml
plantuml:
  theme:
    light: catppuccin/latte
    dark: catppuccin/mocha
```

## Flavors

All four flavors of [catppuccin](https://catppuccin.com/) are implemented for PlantUML
and C4 extension.

???+ note "Special Flavor"

    A special `latte-white` flavor has been added to this theme,
    setting the base color to `#ffffff` instead of catppuccino's `#eff1f5`.
    Some users may find it more appealing when used with light mode.

## Examples

Let's see how various diagrams look with this theme.

### Class Diagram

=== "catppuccin/latte"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/latte.puml

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

=== "catppuccin/frappe"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/frappe.puml

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

=== "catppuccin/macchiato"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/macchiato.puml

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

=== "catppuccin/mocha"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/mocha.puml

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

=== "catppuccin/latte"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/latte.puml

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

=== "catppuccin/frappe"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/frappe.puml

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

=== "catppuccin/macchiato"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/macchiato.puml

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

=== "catppuccin/mocha"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/mocha.puml

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

### Entity

=== "catppuccin/latte"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/latte.puml

    title "Database Entities"

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

=== "catppuccin/frappe"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/frappe.puml

    title "Database Entities"

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

=== "catppuccin/macchiato"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/macchiato.puml

    title "Database Entities"

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

=== "catppuccin/mocha"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/mocha.puml

    title "Database Entities"

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

### Timing

=== "catppuccin/latte"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/latte.puml

    clock   "Clock_0"   as C0 with period 50
    clock   "Clock_1"   as C1 with period 50 pulse 15 offset 10
    binary  "Binary"  as B
    concise "Concise" as C
    robust  "Robust"  as R
    analog  "Analog"  as A


    @0
    C is Idle
    R is Idle
    A is 0

    @100
    B is high
    C is Waiting
    R is Processing
    A is 3

    @300
    R is Waiting
    A is 1
    @enduml
    ```

=== "catppuccin/frappe"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/frappe.puml

    clock   "Clock_0"   as C0 with period 50
    clock   "Clock_1"   as C1 with period 50 pulse 15 offset 10
    binary  "Binary"  as B
    concise "Concise" as C
    robust  "Robust"  as R
    analog  "Analog"  as A


    @0
    C is Idle
    R is Idle
    A is 0

    @100
    B is high
    C is Waiting
    R is Processing
    A is 3

    @300
    R is Waiting
    A is 1
    @enduml
    ```

=== "catppuccin/macchiato"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/macchiato.puml

    clock   "Clock_0"   as C0 with period 50
    clock   "Clock_1"   as C1 with period 50 pulse 15 offset 10
    binary  "Binary"  as B
    concise "Concise" as C
    robust  "Robust"  as R
    analog  "Analog"  as A


    @0
    C is Idle
    R is Idle
    A is 0

    @100
    B is high
    C is Waiting
    R is Processing
    A is 3

    @300
    R is Waiting
    A is 1
    @enduml
    ```

=== "catppuccin/mocha"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/mocha.puml

    clock   "Clock_0"   as C0 with period 50
    clock   "Clock_1"   as C1 with period 50 pulse 15 offset 10
    binary  "Binary"  as B
    concise "Concise" as C
    robust  "Robust"  as R
    analog  "Analog"  as A


    @0
    C is Idle
    R is Idle
    A is 0

    @100
    B is high
    C is Waiting
    R is Processing
    A is 3

    @300
    R is Waiting
    A is 1
    @enduml
    ```

### C4

=== "catppuccin/latte"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/latte.puml

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

=== "catppuccin/frappe"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/frappe.puml

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

=== "catppuccin/macchiato"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/macchiato.puml

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

=== "cattpuccin/mocha"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/catppuccin/mocha.puml

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
