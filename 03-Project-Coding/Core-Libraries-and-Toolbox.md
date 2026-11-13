---
title: Core Libraries and Toolbox
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📦 Core Libraries and Toolbox

## Library Hierarchy
The Bastien-Antigravity platform uses a layered library architecture. Versions are managed per-repository; always refer to the `VERSION.txt` file at each repository root for the current production baseline.

```mermaid
graph TD
    subgraph Toolbox_Layer [Microservice Toolbox]
        MT[Toolbox Core]
        BM[Business Models: MarketEvent, Signal]
    end

    subgraph Config_Layer [Distributed Config]
        DC[Config Engine]
        RSA[RSA Decryption: ENC Pattern]
    end

    subgraph Transport_Layer [Safe-Socket]
        SS[Universal Transport]
        ID[Idle Zombie Detection]
    end

    subgraph Telemetry_Layer [Universal Logger]
        UL[Logger Facade]
        FL[Flexible Logger Engine]
        VBA[VBA Message Pump]
    end

    MT --> DC
    DC --> SS
    UL --> FL
    UL --> DC
```

---
## 1. microservice-toolbox
**Module**: `github.com/Bastien-Antigravity/microservice-toolbox/go`
**Languages**: Go, Rust, Python, C++17, pure C11 (`contracts.h`), VBA
**Role**: The standardized entry point for all microservice bootstrapping, configuration, contracts, telemetry, resilience, and networking. Never reimplement these tools inside microservices.

### Key Features
- **Smart Loader & `AppConfig` (`config`, `bootstrap`)**: Implements the "Hierarchy of Truth" (CLI > ENV > YAML > Config-Server), `BootstrapService` / `init_microservice`, `DecryptSecret`, `OnLiveConfUpdate`, unique-port validation, and **CLI Docker Guard** (`--host`/`--port`/`--grpc_host`/`--grpc_port` ignored inside containers).
- **Business Data Standards**: Unified models defined in `schemas/business`:
    - `MarketEvent`: Low-latency L1/L2 data envelope.
    - `OHLCV`: Standardized time-series bars.
    - `Signal`: Unified strategy signals (Buy/Sell/Exit).
- **Dedicated Versioning (`appConfig.GetVersion()` / `app_config.get_version()`)**: Exposed directly on `AppConfig` across **Go, Python, Rust, C++17, and VBA**, resolving strictly from `VERSION.txt` (fail-fast if missing; zero runtime `APP_VERSION`/`SERVICE_VERSION` overrides, zero `"0.0.1"` fallbacks, and zero ad-hoc `VERSION.txt` scanning loops in services).
- **Declarative `ServiceSpec` & `ExchangeContract`s (`spec`, `contracts`)**: Auto-enriches `URL`, `%s` port substitution in `Framing`, `DataStructure` (`version` via `AppConfig.GetVersion()`, `capability`, `ports`, `node`), `NavRoute`, `Canvas`, and `Health` during `BuildSpecFromConfig` / `PublishWithLifecycle`, plus built-in IDL/route extractors (`ExtractProtoTextOperations`/`extract_proto_operations`, `ExtractCapnpOperations`/`extract_capnp_operations`, `RenderProtoIDL`, `extract_fastapi_operations`) across Go, Python, Rust, C++17, and pure C11 (`contracts.h`).
- **Real-Time Transport WireTap (`wiretap`)**: Lock-free per-edge & segregated channel telemetry (`SetEnabled`/`IsEnabled`, `ConfigureFromConfig`, `RecordEvent`, `Snapshot`) across **Go, Python, Rust, and C++17**, auto-initialized by `BootstrapService` / `init_microservice`.
- **Resilience, Connectivity, Lifecycle & Direct Alerts**: Infinite-retry `conn_manager`, config-verbatim `connectivity.Resolver` (no `0.0.0.0` rewrite), LIFO `lifecycle.Manager`, gRPC `network` server builders, `teleremote` client, NATS `messaging` connector, and `NotificationClient` (via `libnotif`).
- **The Mirroring Mandate**: Go is the source of truth. Features MUST be ported to Python, Rust, and C++ in the same development cycle to maintain parity.

---

## 2. universal-logger
**Module**: `github.com/Bastien-Antigravity/universal-logger`
**Languages**: Go, C++, Python, Rust, VBA (via CGO bridge)
**Role**: Standardized logging facade. Decouples services from the underlying `flexible-logger` engine.

### Advanced Capabilities
- **Shared Dynamic Library**: The Go core is compiled to a shared library (`.dll`, `.so`) used by all language facades.
- **Defensive Marshaling**: Prevents runtime panics by using `yaml:"-"` on internal state fields.
- **VBA Message Pump**: Uses a hidden `HWND_MESSAGE` window to safely bridge multi-threaded Go callbacks into Excel's single-threaded environment.
- **Handle Memory Store**: Tracks sessions via integer handles to minimize FFI overhead.

---

## 3. distributed-config
**Module**: `github.com/Bastien-Antigravity/distributed-config`
**Language**: Go (Reference)
**Role**: YAML-based configuration with environment variable expansion and native RSA decryption.

### Key Features
- **ENC(...) Pattern**: Secrets remain encrypted in memory. Decrypted on-demand via the `DecryptSecret()` API.
- **Error Transparency**: Native support for `GetLastError()` to surface engine-level failures to the language facade.
- **In-Memory Mirroring**: High-performance mirroring ensures sub-millisecond config lookups.

---

## 4. safe-socket
**Module**: `github.com/Bastien-Antigravity/safe-socket`
**Languages**: Go, Python, C API
**Role**: Universal high-performance transport (TCP/UDP/SHM) with **Infinite Wait** resilience.

### Architecture
- **Zombie Detection**: Utilizes adaptive heartbeats to detect dead connections in background streams.
- **Zero-Timeout Reads**: Supports persistent blocking reads while maintaining active health monitoring.

---

## 🔄 Polyglot Development Workflow
Developing across library (parent) and microservice (child) boundaries requires a coordinated ritual.

### 1. Local Override (Simultaneous Dev)
To work on a library and a microservice at the same time without pushing intermediate versions:
- **Go**: Use `go.mod` `replace` directives to point to your local library clone.
- **Python**: Use `pip install -e /path/to/local/lib`.
- **Rust**: Use `[patch.crates-io]` in `Cargo.toml`.

### 2. The Atomic Update Ritual
When a core API change occurs:
1. **Parent Update**: Implement the change in the Go reference library.
2. **Facade Porting**: Immediately port the change to Python, Rust, and C++ facades (Mirroring Mandate).
3. **Integration Test**: Run the `integration/run_tests.sh` suite in the toolbox.
4. **Child Update**: Update the microservice to consume the new library version only after all facades are validated.

---
*Reference: [[01-General-Naming-Conventions]], [[11-Unified-Comment-Standards]]*
