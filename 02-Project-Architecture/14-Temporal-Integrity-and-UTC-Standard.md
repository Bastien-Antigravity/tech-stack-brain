---
microservice: ecosystem-wide
type: architecture
status: active
tags:
- '#zone/3-fleet'
- '#domain/architecture'
- '#layer/standard'
- '#type/architecture'
- '#state/active'
---

# 14. Temporal Integrity & Universal UTC Standard

## 1. Executive Summary & Core Mission
In a high-throughput, distributed financial microservices ecosystem spanning multiple physical hosts, cloud VPS environments, Docker networks, and heterogeneous programming runtimes (Go, Python, Rust, C++, JavaScript, VBA), **temporal integrity is paramount**.

Clock skew, ambiguous local timezones, daylight saving transitions (DST), and timezone-naive datetime objects lead to silent data corruption, broken backtest alignment, mismatched log ordering, and invalid trade executions.

Therefore, the Bastien-Antigravity ecosystem enforces a strict, fleet-wide **100% UTC Mandate**.

---

## 2. The 100% UTC Invariant Rule
1. **Zero Local Time Ingestion or Storage**: No system log, telemetry packet, database row, serialized event, or wire message may be recorded, formatted, or transmitted in local server time.
2. **Explicit UTC Declarations**: Formatted timestamps in human-facing interfaces, CLI tools, and web dashboards must explicitly display the `UTC` or `Z` suffix (e.g. `14:32:05 UTC` or `2026-11-02T22:45:00.000000000Z`).
3. **Timezone-Aware Serialization**: Wire formats (JSON, Cap'n Proto, Protobuf, MsgPack) must serialize timestamps either as Unix epoch nanoseconds/milliseconds or ISO 8601 strings in UTC (`YYYY-MM-DDTHH:MM:SS.fffffffffZ`).

---

## 3. Polyglot Language Implementation Standards

### 3.1. Go (`microservice-toolbox`, `web-interface`, `config-server`, `notif-server`, `watchdog-agent`)
- **Mandate**: When constructing timestamps for serialization, logging, or display, **always call `.UTC()`**.
- **Prohibited Anti-Pattern**: Bare `time.Now().Format(...)` or storing `time.Now()` into a JSON struct without `.UTC()`.
  ```go
  // ❌ STRICTLY PROHIBITED (Local timezone leakage)
  nowStr := time.Now().Format(time.RFC3339)
  s.RegisteredAt = time.Now()
  
  // ✅ MANDATORY STANDARD (Guaranteed UTC with 'Z')
  nowStr := time.Now().UTC().Format(time.RFC3339)
  s.RegisteredAt = time.Now().UTC()
  ```
- **Monotonic Clocks**: Monotonic elapsed durations (`time.Since(start)`) are permitted for performance benchmarks, but must never be serialized across the wire.
- **AST Verification**: Enforced automatically via `TestArchitectureHygiene_ASTEnforcement` in CI test suites.

---

### 3.2. Python (`08-Squad-Agent`, `09-RAG-Engine`, `docker-deployment/ghcr`)
- **Mandate**: All datetime operations must be **timezone-aware in UTC**.
- **Prohibited Anti-Patterns**:
  - `datetime.now()` without a timezone parameter (produces naive local time).
  - `datetime.utcnow()` (deprecated in Python 3.12+; produces naive UTC without tzinfo).
  - `time.localtime()` or `time.strftime` without explicit UTC struct_time.
  ```python
  # ❌ STRICTLY PROHIBITED
  now = datetime.now()
  now = datetime.utcnow()
  
  # ✅ MANDATORY STANDARD (Python 3.12+)
  from datetime import datetime, timezone
  now = datetime.now(timezone.utc)
  iso_str = now.isoformat()
  ```

---

### 3.3. Rust (`log-server`)
- **Mandate**: All internal log timestamps, file flushes, and socket packets must strictly use `chrono::Utc`.
- **Prohibited Anti-Pattern**: `chrono::Local` or `Local::now()`.
  ```rust
  // ❌ STRICTLY PROHIBITED
  use chrono::Local;
  let timestamp = Local::now().format("%Y-%m-%dT%H:%M:%S%.9fZ").to_string(); // Slapping 'Z' on local time!
  
  // ✅ MANDATORY STANDARD
  use chrono::Utc;
  let timestamp = Utc::now().format("%Y-%m-%dT%H:%M:%S%.9fZ").to_string();
  ```

---

### 3.4. Web Interface & Client JavaScript (`web-interface`)
- **Mandate**: All topbar clocks, status badges, inspector tabs, charts, and table timestamps must render in UTC.
- **Prohibited Anti-Patterns**:
  - `new Date().toLocaleTimeString()` or `new Date().toLocaleString()` without `{ timeZone: 'UTC' }`.
  - `new Date().getHours()` / `new Date().getMinutes()` for displaying time without UTC getters.
  - `new Date().toTimeString().split(' ')[0]` (local client time).
  ```javascript
  // ❌ STRICTLY PROHIBITED (Browser local timezone divergence)
  clock.textContent = now.toDateString() + ' ' + now.getHours() + ':' + now.getMinutes();
  
  // ✅ MANDATORY STANDARD
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  clock.textContent = `${days[now.getUTCDay()]} ${months[now.getUTCMonth()]} ${('0' + now.getUTCDate()).slice(-2)} ${now.getUTCFullYear()} ${('0' + now.getUTCHours()).slice(-2)}:${('0' + now.getUTCMinutes()).slice(-2)} UTC`;
  
  // Or via Formatter utility
  Formatter.date(d, { timeZone: 'UTC' });
  Formatter.time(d); // Formats HH:MM:SS UTC using getUTCHours/Minutes/Seconds
  ```

---

### 3.5. Database & TimescaleDB
- **Mandate**: All timestamp table columns across PostgreSQL and TimescaleDB must use `TIMESTAMPTZ` (`TIMESTAMP WITH TIME ZONE`).
- **Session Configuration**: All service connections must operate with timezone set to UTC:
  ```sql
  SET TIME ZONE 'UTC';
  ```
- **Queries**: Ad-hoc queries referencing current time must use `NOW() AT TIME ZONE 'UTC'`.

---

## 4. Automated Compliance & Detection Strategy
To ensure zero regression across the ecosystem, automated checks are integrated into:
1. **AST Hygiene Tests (`go test ./...`)**: Inspects Go AST trees for bare `time.Now().Format` calls.
2. **Ripgrep Preflight Audits**:
   - Go: `rg "time\.Now\(\)\.Format"`
   - Python: `rg "datetime\.now\(\)"` and `rg "datetime\.utcnow\(\)"`
   - Rust: `rg "chrono::Local"`
   - Web/JS: `rg "\.toLocaleTimeString\(\)"` (ensures `timeZone: 'UTC'` is present).
3. **CI/CD Quality Gates**: Enforced in `master-ci.yml` across all pull requests and merges.
