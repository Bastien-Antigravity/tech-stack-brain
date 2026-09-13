---
microservice: ecosystem-wide
type: architecture
status: active
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# Configuration Standards: Profiles, Toolbox & Capabilities

## Configuration Philosophy
Our microservices avoid hardcoded parameters. All settings are sourced from a layered configuration system managed by `microservice-toolbox`.

### 1. Configuration Loading via Microservice-Toolbox
- **The Interface**: `microservice-toolbox` is the **Universal Entry Point** for all services. To ensure performance and portability, it provides native implementations for each language while maintaining strict API parity.
- **The Engine**: In Go, the toolbox wraps `distributed-config`. In Python and Rust, the toolbox provides a native implementation of the same standard.
- **Entry Point**: ALL services must use `microservice-toolbox` to load configuration:
  - Go: `config.LoadConfig("standalone", nil)` → returns `*AppConfig`
  - Rust: `microservice_toolbox::config::load_config("standalone")` → returns `Result<AppConfig>`
  - Python: `load_config("standalone")` → returns `AppConfig`
- **Profiles**:
  - `standalone` / `test` → **Dev Mode**: Local YAML file is the hard override.
  - Any other profile → **Production Mode**: Config Server is authoritative; local file fills gaps (e.g., local overrides).
- **Search Paths (Locality Rule)**: To ensure predictability, configuration loaders MUST prioritize the **Binary's Home Directory** over the Current Working Directory (CWD).
  - **Auto-Skeleton (Zero-Config)**: If the target config file (e.g., `standalone.yaml`) is missing, the library automatically generates a complete, platform-standard skeleton in the binary's folder.
  - **'go run' Support**: For development, the system robustly detects the source file directory (`cmd/<service>/`) and treats it as the home folder for configs and logs.

### 2. Harmonized Configuration System (v2.0+)
The fleet utilizes a **Universal Configuration Template** located in `docker-deployment/modes/local/config/native.yaml`.
- **Single Source of Truth**: All repositories symlink their local `standalone.yaml` directly to this authoritative profile.
- **Environment Driven**: The YAML uses `${VAR:-default}` templates for all IP addresses and ports, allowing a single file to support Local, Docker, and isolated macOS (`127.0.0.2`) deployments simultaneously.
- **The "Chain of Truth" (Priority)**:
  1. **Environment Variables**: Highest priority (forced overrides).
  2. **Config File**: Canonical source for static settings.
  3. **Hardcoded Fallbacks**: Safe defaults (`127.0.0.1`) used for skeleton generation.

### 3. Unified Shared Engine Architecture (v1.9.92+)
- To ensure absolute behavioral parity and memory-space unification, all non-Go languages (Python, Rust, C++, VBA) utilize the **Unified Shared Engine** (`libdistconf` / `libunilog`).
- **Single Memory State**: The shared engine ensures that multiple configuration sessions (e.g., one in the Logger and one in the Toolbox) share the same handle store and runtime environment.
- **Shared Logic**: By converging on the `src/cgo_bridge` core in `distributed-config`, all languages benefit from the exact same environment expansion, path discovery, and network sync logic.
- **Critical Rule (FFI Stability)**: When wrapping the shared engine, the library MUST NOT be unloaded (`dlclose`). See [Hidden Patterns and Gotchas](../../03-Project-Coding/07-Hidden-Patterns-and-Gotchas.md) for details.

### 3. Priority Hierarchy (Highest → Lowest)
1. **CLI Flags** (parsed by `microservice-toolbox` automatically)
2. **Local YAML File** (profile-dependent merge)
3. **Config Server** (via `distributed-config` sync)
4. **Environment Variables** (template expansion in YAML)

### 4. Standard CLI Arguments
The toolbox provides these flags automatically in all languages:

| Flag | Type | Description |
|---|---|---|
| `--name` | string | Service name identifier |
| `--host` | string | Binding host IP |
| `--port` | int | Binding port |
| `--grpc_host` | string | gRPC binding host IP |
| `--grpc_port` | int | gRPC binding port |
| `--conf` | string | Path to configuration file |
| `--log_level` | string | Logging level (DEBUG, INFO, etc.) |
| `--key` | string | Path to RSA Public/Private key (Utilities only) |

#### **Utility Tooling Convention**
Utilities located in `/cmd` (e.g., `config-tool`) MUST follow the same flag-based philosophy. Positional arguments should be avoided.
- **Incorrect**: `config-tool encrypt public.pem "secret"`
- **Correct**: `config-tool encrypt --key public.pem --token "secret"`

### 5. Docker Guard
When running inside Docker (detected via `/.dockerenv` or `DOCKER_ENV` env var), all CLI network overrides (`--host`, `--port`, `--grpc_host`, `--grpc_port`) are **silently ignored** to preserve Docker's DNS-based service discovery.

### 6. Capability-Based Configuration
Configuration is organized around **capabilities** — named service entries in YAML:
```yaml
capabilities:
  log_server:
    ip: "127.0.0.1"
    port: "9020"
  timescale_db:
    ip: "127.0.0.1"
    port: "5432"
    user: "dbuser"
    password: "dbuser"
    dbname: "maindb"
```
- **Access Pattern (Go)**: Use `cfg.GetCapability("timescale_db", &dbConfig)` to unmarshal into a typed struct.
- **Access Pattern (Rust)**: Use `ac.get_listen_addr("log_server")` to get `ip:port` strings.
- **Access Pattern (Python)**: Use `ac.get_listen_addr("log_server")` for the same.

### 7. Environment Variable Expansion
YAML files support environment variable templates using `${VAR_NAME:-default}` syntax. These are expanded at load time by `distributed-config`.

### 8. Non-Shared & Local Configuration
When configuration settings must remain private to a single microservice rather than shared ecosystem-wide, three distinct mechanisms are supported:

1. **The `local:` YAML Block**:
   - For settings that do not fit the shared `capabilities` pattern (e.g., service-internal directories, operational flags).
   - **Strictly Non-Synchronized**: The `local:` block is **never** synchronized with or broadcast by the `config-server`. It lives exclusively in the local service YAML file.
   - **Access Pattern (Go/C++)**: Access via `ac.GetLocal("key")` or unmarshal the entire block into a struct using `UnmarshalLocal(&target)`.
   - **Access Pattern (Python/Rust)**: Access via `ac.get_local("key")` or `unmarshal_local::<T>()`.
   - **Secret Protection**: Values inside `local:` can also use `ENC(...)` and are decrypted on-demand via `DecryptSecret()`.

2. **Dedicated Service Config Files**:
   - Each service can specify a standalone configuration file via `--conf /path/to/service.yaml` or through its binary-local `<service-name>.yaml`.
   - In `standalone` or `test` profiles, this local file is authoritative and acts as a complete, unshared override.

3. **Scoped Environment Variables**:
   - `${VAR_NAME:-default}` template placeholders in YAML resolve from the process environment.
   - Variables set exclusively inside a service's Docker container or systemd unit remain completely isolated from other services.

### 9. Secret Encryption & Per-Service Key Architecture (v1.9.1+)
`distributed-config` provides native RSA encryption for sensitive fields in YAML configurations:
- **Format**: Wrap base64-encoded ciphertext in `ENC(...)`. Example: `token: "ENC(base64_blob)"`.
- **Zero-Knowledge Core**: `config-server` and `web-interface` do NOT decrypt secrets. Configuration loaders (`distributed-config` / `microservice-toolbox`) preserve `ENC(...)` values untouched in the configuration AST and in-memory snapshots.
- **On-Demand Decryption**: Consuming microservices explicitly decrypt secrets at point-of-use using `appConfig.DecryptSecret(ciphertext)` (or `secret.Decrypt(ciphertext)`).
- **Per-Service Private Key Isolation**:
  - Each microservice can possess its own unique RSA key pair (e.g. `tele-remote-public.pem` / `tele-remote-private.pem`).
  - Secrets encrypted with a specific service's public key can **only** be decrypted by that specific service.
  - A compromise of one service's private key does not compromise secrets encrypted for other services.
- **Key Resolution Hierarchy**:
  1. `BASTIEN_PRIVATE_KEY` (inline PEM string in environment)
  2. `BASTIEN_PRIVATE_KEY_PATH` (or `--key` CLI argument)
  3. `/etc/bastien/private.pem` (Production default / Docker secret mount)
  4. `./private.pem` (Local development fallback)
- **Volatility Rule**: Decrypted values must never be written to disk, logs, or distributed back to `config-server`. Services must retain decrypted secrets only in volatile memory for the duration of the connection or operation.
- **Unified Tooling**: All key generation and encryption tasks are performed using `config-tool` (`distributed-config/cmd/config-tool`).

### 10. Polyglot Feature Parity Matrix

| Feature | Go | Python | Rust | C++ | VBA |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Layered YAML Loading | ✅ | ✅ | ✅ | ✅ | ✅ |
| `config/` Directory Fallback | ✅ | ✅ | ✅ | ✅ | ✅ |
| CLI Flag Overrides | ✅ | ✅ | ✅ | ✅ | ✅ |
| Environment Var Expansion | ✅ | ✅ | ✅ | ✅ | ✅ |
| RSA Secret Decryption | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Absolute Parity (v1.9.9)** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **UnmarshalLocal** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Error Transparency** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Remote Config Sync** | ✅ | ✅ (CGO) | ✅ (CGO) | ✅ (CGO) | ✅ (CGO) |

### 11. Error Transparency (v1.9.9+)
All `microservice-toolbox` implementations must surface raw engine-level errors from the underlying `distributed-config` bridge.
- **Strict Exception Handling**: Toolboxes should **throw/raise/return** the exact error string retrieved from `GetLastError()` on bridge failure.
- **No Silencing**: Swallowing bridge errors (e.g., returning original ciphertext on decryption failure) is strictly forbidden.

> [!NOTE]
> **RSA Encryption (`ENC(...)`)** is now a cross-language standard. You can safely use encrypted secrets in shared configuration files across the entire fleet.
