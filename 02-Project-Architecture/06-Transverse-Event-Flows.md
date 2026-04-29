---
type: architecture
tags:
  - domain/architecture
  - domain/networking
---

# 🌀 Transverse Event Flow sequences

This document physically maps the boundaries and interactions between isolated microservices to provide a true transversal C4 view.

## Scenario: Client pushing configuration update

This sequence demonstrates standard communication:
1. TCP Handshakes (`safe-socket`)
2. Business Logic Execution (`config-server`)
3. Global Broadcast Notification (`safe-socket`)
4. Asynchronous logging execution (`log-server`)

```mermaid
sequenceDiagram
    participant Client as App-Client
    participant SSConfig as safe-socket (Transport)
    participant CS as config-server
    participant FlexLog as flexible-logger
    participant LS as log-server

    %% 1. Handshake Phase
    Client->>SSConfig: Connect (TCP)
    SSConfig-->>Client: Request Identity Header
    Client->>SSConfig: Send `Profile=tcp-hello`, `Name=ClientA`
    SSConfig->>CS: Validated Connection

    %% 2. Action Triggered
    Client->>CS: Action/Update Config "PORT=8000"
    CS->>CS: Process Request (Atomic Swap)
    
    %% 3. Trigger Local Logging
    CS->>FlexLog: appLogger.Info("Config updated")
    
    %% 4. Asynchronous Remote Log Push
    par Flexible Logging
        FlexLog-->>LS: Push Unilog Packet [TCP/Safe-Socket]
        LS->>LS: Write to logstore.db
    end

    %% 5. Global Config Broadcast
    par Distributed Broadcast
        CS-->>Client: Propagate_Update "PORT=8000"
        CS-->>Other_Clients: Propagate_Update "PORT=8000"
    end
```
