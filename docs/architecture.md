# Architecture

> Reference for your team. You don't need to redraw it, but you do need to follow it:
> the change request is much easier when rules live in services and SQL lives in repositories.

Panther Parking uses a **layered architecture** (Sommerville Ch. 6). Each layer may call only the layer directly below it.

```mermaid
flowchart TD
    Browser["Browser (HTML pages)"]
    subgraph Presentation["Presentation layer: app/routes/ + app/templates/"]
        AuthRoutes["auth.py"]
        LotRoutes["lots.py"]
        VehicleRoutes["vehicles.py"]
        PermitRoutes["permits.py"]
    end
    subgraph Business["Business layer: app/services/"]
        AuthService["auth_service.py"]
        LotService["lot_service.py"]
        VehicleService["vehicle_service.py"]
        PermitService["permit_service.py"]
    end
    subgraph Data["Data access layer: app/repositories/"]
        UserRepo["user_repository.py"]
        LotRepo["lot_repository.py"]
        VehicleRepo["vehicle_repository.py"]
        PermitRepo["permit_repository.py"]
    end
    DB[("SQLite database")]

    Browser --> AuthRoutes & LotRoutes & VehicleRoutes & PermitRoutes
    AuthRoutes --> AuthService
    LotRoutes --> LotService
    VehicleRoutes --> VehicleService
    PermitRoutes --> PermitService
    AuthService --> UserRepo
    LotService --> LotRepo
    VehicleService --> VehicleRepo
    PermitService --> PermitRepo & VehicleRepo & LotRepo
    UserRepo & LotRepo & VehicleRepo & PermitRepo --> DB
```

## Rules for each layer

| Layer | May do | May not do |
| --- | --- | --- |
| Routes | Read the request, call one service function, render a template or redirect | Contain business rules or SQL |
| Services | Enforce business rules (validation, status, eligibility) | Touch `request`, `session`, or write SQL |
| Repositories | Run SQL and return plain dicts | Make business decisions |
