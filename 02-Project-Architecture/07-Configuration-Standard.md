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
  - Any other profile → **Production Mode**: Config Server is authoritative; local file fills gaps.

### 2. Priority Hierarchy (Highest → Lowest)
1. **CLI Flags** (parsed by `microservice-toolbox` automatically)
2. **Local YAML File** (profile-dependent merge)
3. **Config Server** (via `distributed-config` sync)
4. **Environment Variables** (template expansion in YAML)

### 3. Standard CLI Arguments
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

### 4. Docker Guard
When running inside Docker (detected via `/.dockerenv` or `DOCKER_ENV` env var), all CLI network overrides (`--host`, `--port`, `--grpc_host`, `--grpc_port`) are **silently ignored** to preserve Docker's DNS-based service discovery.

### 5. Capability-Based Configuration
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

### 6. Environment Variable Expansion
YAML files support environment variable templates using `${VAR_NAME:-default}` syntax. These are expanded at load time by `distributed-config`.

### 8. Private Configuration (Local Only)
For settings that do not fit the `ip/port` capability pattern (e.g., custom service-specific flags, internal paths), use the `private:` block. This section is **Toolbox-Specific** and is strictly **Local-Only**:
- **Non-Synchronized**: Unlike `capabilities`, the `private:` block is **never** synchronized with the Config Server. It remains private to the service instance.
- **Access Pattern (Go)**: Access via `ac.Private` (e.g., `ac.GetPrivate("worker_count")`).
- **Access Pattern (Rust/Python)**: Access via `ac.data["private"]`.
- **Decryption**: Private values are eligible for on-demand `ENC(...)` decryption using toolbox helpers.

### 9. Secret Encryption (v1.9.1+)
`distributed-config` supports native RSA encryption for sensitive fields in YAML files.
- **Pattern**: Wrap encrypted values in `ENC(...)`. Example: `password: "ENC(base64_blob)"`.
- **On-Demand Decryption**: By default, the library **stores secrets in their encrypted form**. The service must explicitly decrypt them when needed using the toolbox helpers.
- **Public Key Discovery**: At boot, the system searches for `public.pem` (following the standard discovery chain) and, if found, embeds its content into the `common.public_key` config field. This allows the service to share its public identity without manual configuration.
- **Key Locations**:
  - **Public Key (`public.pem`)**: Non-Sensitive. Used by developers to encrypt secrets.
  - **Private Key (`private.pem`)**: Critical Secret. **MUST NOT** be committed to Git. loaded from `BASTIEN_PRIVATE_KEY_PATH` or `/etc/bastien/`.
- **Volatility Rule**: Decrypted values must never be written to disk, logs, or databases. Services should keep decrypted secrets in volatile variables for the shortest time possible.
- **Utilities**: All repositories must include or reference the standard **`config-tool`** found in the `distributed-config/cmd` directory for managing these secrets.

### 10. Polyglot Feature Parity Matrix

| Feature | Go | Python | Rust | C++ | VBA |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Layered YAML Loading | ✅ | ✅ | ✅ | ✅ | ✅ |
| CLI Flag Overrides | ✅ | ✅ | ✅ | ✅ | ✅ |
| Environment Var Expansion | ✅ | ✅ | ✅ | ✅ | ✅ |
| **RSA Secret Decryption** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Remote Config Sync** | ✅ | ✅ (CGO) | ✅ (CGO) | ✅ (CGO) | ✅ (CGO) |

> [!NOTE]
> **RSA Encryption (`ENC(...)`)** is now a cross-language standard. You can safely use encrypted secrets in shared configuration files across the entire fleet.
