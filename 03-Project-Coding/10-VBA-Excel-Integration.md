---
title: VBA Excel Integration
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
- '#tech/vba'
---
# 📐 VBA Excel Integration

## Architectural Rule
- **Paradigm**: Event-driven automation for Excel-based reporting and fleet monitoring.
- **FFI Integration**: Use `Declare PtrSafe Sub/Function` to bind to the standard `libdistconf.dll`, `libunilog.dll`, and `libnotif.dll` bridges.
- **Error Handling**: Every public Sub/Function MUST use the `On Error GoTo ErrorHandler` pattern to ensure FFI resources are handled gracefully.
- **State Management**: Use **Global Singleton Objects** in a dedicated `MTB_Core` module for accessing the Configuration Store and the Universal Logger.
- **Static Discovery**: The VBA toolbox must search for the `private.pem` key in the standard system locations (`/etc/bastien/` or `%APPDATA%\Bastien\`) to enable RSA decryption.

## 🛠 Construction & Implementation
- **Module Separation**: Business logic MUST be separated from DLL declaration modules.
- **Cleanup Ritual**: Always release objects and clear handles in the `ExitPoint` of your procedures.

## 🏷 Naming Conventions
- **Procedures**: `PascalCase` — `ProcessReport`, `SyncConfiguration`.
- **Variables**: `camelCase` — `rowIdx`, `configHandle`.
- **Global Constants**: `SCREAMING_SNAKE_CASE`.

## 📦 Standard VBA Toolbox Usage (`AppConfig.cls` & `NotificationClient.cls`)
```vba
' Import AppConfig.cls, NotificationClient.cls, DistConf.bas, Toolbox.bas
Public Sub SyncAppConfig()
    On Error GoTo ErrorHandler

    Dim ac As New AppConfig
    ac.LoadConfig "standalone"

    Debug.Print ac.GetVersion()
    Debug.Print ac.GetListenAddr("market_observer")

    Dim notif As NotificationClient
    Set notif = Toolbox.NewNotificationClientFromConfig(ac)
    notif.Send "VBA workbook synchronized", "telegram"

ExitPoint:
    Exit Sub
ErrorHandler:
    MsgBox "Toolbox Runtime Error: " & Err.Description, vbCritical
    Resume ExitPoint
End Sub
```

## Motivation (Why?)
- Integration: Bridges high-performance microservices with human-centric Excel reporting workflows.
- Stability: Standardized error handling prevents silent failures in financial or operational spreadsheets.
- Parity: Ensures VBA tools use the exact same configuration and secrets as the rest of the fleet.

---
*Reference: [[07-Configuration-Standard]], [[05-Project-Scripts/Hide-Empty-Folders.py]]*
