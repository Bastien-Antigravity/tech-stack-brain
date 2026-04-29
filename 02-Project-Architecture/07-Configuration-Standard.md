# Configuration Standards: Profiles, Toolbox & Capabilities

## Configuration Philosophy
Our microservices avoid hardcoded parameters. All settings are sourced from a layered configuration system managed by `microservice-toolbox`.

### 1. Configuration Loading via Microservice-Toolbox
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

### 7. Service Metadata
- **Name**: Always include a `common.name` field for service identification. This is set automatically by the `--name` CLI flag.
- **Config Server**: For production deployments, services sync their configuration from the centralized `config-server` via gRPC.
