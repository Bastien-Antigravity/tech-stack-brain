---
title: "Interface Contracts"
type: architecture
status: active
microservice: ecosystem-wide
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

### `notif-server/interfaces.Notificator`
```
Send(msg *utils.NotifMessage)
SendRaw(data []byte)
LoadNotifSender(notifiersConf) -> map[string][]string
```

---

## Cross-Language Parity

| Method | Go | Rust | Python |
|--------|-----|------|--------|
| Load config | `LoadConfig(profile, flags)` | `load_config(profile)` | `load_config(profile, flags)` |
| Listen addr | `GetListenAddr(cap)` | `get_listen_addr(cap)` | `get_listen_addr(cap)` |
| gRPC addr | `GetGRPCListenAddr(cap)` | `get_grpc_listen_addr(cap)` | `get_grpc_listen_addr(cap)` |
| Deep merge | `DeepMerge(dst, src)` | `deep_merge(dst, src)` | `deep_merge(dst, src)` |
| Safe logger | `EnsureSafeLogger(l)` | `ensure_safe_logger(l)` | `ensure_safe_logger(l)` |

> **Rule**: Go is the source of truth. Rust and Python implement identical semantics.
