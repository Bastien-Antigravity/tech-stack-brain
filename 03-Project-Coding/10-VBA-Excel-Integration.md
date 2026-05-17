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
- **FFI Integration**: Use `Declare PtrSafe Sub/Function` to bind to the standard `libdistconf.dll` and `libunilog.dll` bridges.
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

## 📦 FFI Declarations Example
```vba
' Module: MTB_Bridge
#If Win64 Then
    Public Declare PtrSafe Function Toolbox_LoadConfig Lib "libdistconf.dll" (ByVal profile As String, ByVal path As String) As LongPtr
    Public Declare PtrSafe Function Toolbox_GetLastError Lib "libdistconf.dll" () As String
#Else
    Public Declare Function Toolbox_LoadConfig Lib "libdistconf.dll" (ByVal profile As String, ByVal path As String) As Long
#End If

' Usage Pattern
Public Sub SyncAppConfig()
    On Error GoTo ErrorHandler
    
    Dim hnd As LongPtr
    hnd = Toolbox_LoadConfig("standalone", "")
    
    if hnd = 0 Then
        MsgBox "Config Error: " & Toolbox_GetLastError(), vbCritical
    End If
    
ExitPoint:
    Exit Sub
ErrorHandler:
    MsgBox "VBA Runtime Error: " & Err.Description
    Resume ExitPoint
End Sub
```

## Motivation (Why?)
- Integration: Bridges high-performance microservices with human-centric Excel reporting workflows.
- Stability: Standardized error handling prevents silent failures in financial or operational spreadsheets.
- Parity: Ensures VBA tools use the exact same configuration and secrets as the rest of the fleet.

---
*Reference: [[07-Configuration-Standard]], [[05-Project-Scripts/Hide-Empty-Folders.py]]*
