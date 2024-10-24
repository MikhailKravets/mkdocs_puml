# Default

Default PlantUML theme that contains `light` and `dark` flavors.

[:material-github: Open Styles on GitHub](https://github.com/MikhailKravets/mkdocs_puml/tree/themes/themes/default){ .md-button }

=== "default/light"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/default/light.puml

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

=== "default/dark"

    ```plantuml
    @startuml
    !include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/default/dark.puml

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

## How to use

In order to use this theme with `mkdocs_puml`, set `theme` config of the plugin as follows:

```yml
theme:
    light: default/light
    dark: default/dark
```

## Examples

This theme is actually identical to the default PlantUML theme, so there’s no need to replicate all the examples here. The only difference lies in C4.

### C4

The `default/dark` flavor enhances the visibility of [C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML).

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
!include https://raw.githubusercontent.com/MikhailKravets/mkdocs_puml/themes/themes/default/dark.puml

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
