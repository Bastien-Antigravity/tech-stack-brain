---
title: Interface Contracts
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📐 Interface Contracts

## Logger Ecosystem (3 Layers)

### Layer 1: `flexible-logger/interfaces.Logger` (Engine)
```
Debug / Info / Warning / Error / Critical
Stream / Logon / Logout / Trade / Schedule / Report  (Domain-specific)
Log(level, format, args)
SetLevel(level)
SetCallerSkip(skip int)
Close()
```

### Layer 2: `universal-logger/interfaces.Logger` (Facade — Superset)
Wraps `flexible-logger` and adds:
```
GetNotifQueue() <-chan *NotifMessage
SetLocalNotifQueue(chan *NotifMessage)
SetMetadata(map[string]string)
AddMetadata(key, value string)
```

> **Rule**: `universal-logger.Logger` is a **strict superset** of `flexible-logger.Logger`.

---

## Socket Ecosystem

### `safe-socket/interfaces.Socket`
```
Common:    Close(), SetLogger()
Client:    Open(), Send(), Write(), Read(), Receive()
Server:    Listen(), Accept() -> TransportConnection
Deadlines: SetDeadline(), SetReadDeadline(), SetWriteDeadline()
```

### `safe-socket/interfaces.SocketProfile`
```
GetName() string
GetAddress() string
GetTransport() TransportType   // FramedTCP | UDP | SharedMemory
GetProtocol() ProtocolType     // none | hello
GetConnectTimeout() int
```

---

## Config Ecosystem

### `distributed-config/interfaces.ConfigStrategy`
```
Name() string
Load(cfg *core.Config) error
Sync(cfg *core.Config) error
GetHandler() *network.ConfigProtoHandler
```

### `microservice-toolbox.AppConfig` (Wrapper)
```
*distconf.Config  (embedded)
Resolver, Profile, Logger
LoadConfig() / LoadConfigWithLogger()
GetListenAddr(capability) -> (string, error)
GetGRPCListenAddr(capability) -> (string, error)
```

---

## Notification Ecosystem

### `microservice-toolbox NotificationClient` (Go, Python, Rust, C++, VBA Parity)
```
Go:     NewClient(appConfig, logger) -> (*NotificationClient, error)
        Send(ctx, message, tags...) -> error
        SendAlert(ctx, level, message, tags...) -> error
        SendWithAttachment(ctx, level, message, attachment, tags...) -> error
        Close() -> error

Python: NotificationClient.from_config(app_config, logger) -> NotificationClient
        await send(message, *tags)
        await send_alert(level, message, *tags)
        await send_with_attachment(level, message, attachment, *tags)
        await close()

Rust:   NotificationClient::from_config(&app_config, logger) -> Result<NotificationClient, String>
        send(&self, message, tags).await -> Result<(), String>
        send_alert(&self, level, message, tags).await -> Result<(), String>
        send_with_attachment(&self, level, message, attachment, tags).await -> Result<(), String>
        close(&self)

C++:    NotificationClient::FromConfig(app_config, logger) -> NotificationClient
        Send(message, tags) -> bool
        SendAlert(level, message, tags) -> bool
        SendWithAttachment(level, message, attachment, tags) -> bool
        Close()

VBA:    Toolbox.NewNotificationClientFromConfig(cfg) -> NotificationClient
        client.Send(message, tagsCSV) -> Boolean
        client.SendAlert(level, message, tagsCSV) -> Boolean
        client.SendWithAttachment(level, message, attachment, tagsCSV) -> Boolean
        client.CloseClient()
```
> **Contract**: `NewClient` / `from_config` / `FromConfig` / `NewNotificationClientFromConfig` dynamically resolves `notif_server` via `GetGRPCListenAddr("notif_server")` / `get_grpc_listen_addr` and strictly fails fast if unresolvable. Zero silent fallback.

### `notif-server/interfaces.Notificator`
```
Send(msg *utils.NotifMessage)
SendRaw(data []byte)
LoadNotifSender(notifiersConf) -> map[string][]string
```

### Ingestion Wire Protocols
- **gRPC Protobuf (Port `1027`)**: `NotifService.SendNotification(NotifRequest) -> NotifResponse`
- **SafeSocket TCP (Port `1026`)**: 4-byte length prefixed Cap'n Proto `NotifierMsg` (via `flexible-logger`)
- **Polyglot Bridge**: Python, Rust, C++, and VBA dispatch to Port `1027` via the Go CGO bridge `libnotif` C ABI (`Notif_Send`, `Notif_SendWithTimeout`) built by `notif-server`. Go services use native Go gRPC directly.

---

## Cross-Language Parity

| Method | Go | Rust | Python | C++ | VBA |
|--------|-----|------|--------|-----|-----|
| Load config | `LoadConfig(profile, flags)` | `load_config(profile)` | `load_config(profile, flags)` | `LoadConfig(profile, flags)` | `LoadConfig(profile)` |
| Listen addr | `GetListenAddr(cap)` | `get_listen_addr(cap)` | `get_listen_addr(cap)` | `GetListenAddr(cap)` | `GetListenAddr(cap)` |
| gRPC addr | `GetGRPCListenAddr(cap)` | `get_grpc_listen_addr(cap)` | `get_grpc_listen_addr(cap)` | `GetGRPCListenAddr(cap)` | `GetGRPCListenAddr(cap)` |
| Deep merge | `DeepMerge(dst, src)` | `deep_merge(dst, src)` | `deep_merge(dst, src)` | `DeepMerge(dst, src)` | In-Memory Mirror |
| Safe logger | `EnsureSafeLogger(l)` | `ensure_safe_logger(l)` | `ensure_safe_logger(l)` | `EnsureSafeLogger(l)` | - |
| Notif Client | `NewClient(ac, l)` | `from_config(ac, l)` | `from_config(ac, l)` | `FromConfig(ac, l)` | `NewNotificationClientFromConfig(cfg)` |
| Send Alert | `SendAlert(ctx, lvl, msg, ...)` | `send_alert(lvl, msg, tags)` | `send_alert(lvl, msg, *tags)` | `SendAlert(lvl, msg, tags)` | `SendAlert(lvl, msg, tagsCSV)` |

> **Rule**: Go is the source of truth. Rust, Python, C++, and VBA implement 100% identical semantics. `EnsureSafeLogger` panics/throws in strict mode (`STRICT_LOGGER=true`). Python, Rust, C++, and VBA integrate with notif-server via the compiled `libnotif` C ABI bridge from `notif-server`.


