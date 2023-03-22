
# Hello Plant UML

Here you see rendered svg diagram.

```puml
@startuml sign_in_sequence

title "Sign In Sequence Diagram"

actor User

participant AppDeviceTokenObtainPairView
participant "@action authenticate" as authenticate

entity AppDevice
entity User as UserModel

User -> authenticate: {"email": email, "password": password}
activate authenticate

authenticate -> UserModel: Look for User with email in DB
activate UserModel

@enduml
```

Text under diagram.

## The second diagram

```puml
@startuml sign_in_objects

title "Sign In Objects"

top to bottom direction

package user_devices {
    package models as device_models {
        class AppDevice {
            Django model to keep the required information
            about user's authenticator app
            ..
            +user: OneToOne[User]
            +secret_key: str
        }
        AppDevice --o AppDevicePairSerializer
    }

}

@enduml
```

## This is the third diagram using custom keyword

```plantuml
@startuml
A -> B
@enduml
```

And here is just code

```python
print("Hello world")
```
