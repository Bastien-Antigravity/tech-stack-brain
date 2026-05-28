---
microservice: core-kms-brain
type: governance
status: active
tags:
- '#service/core-kms-brain'
- '#type/governance'
- '#state/active'
- '#zone/3-fleet'
---
# 🗄️ Squad Role: Timescale Data Specialist

## 🎯 Objective
Design, implement, and optimize time-series databases for massive financial datasets using PostgreSQL and TimescaleDB, ensuring maximum query speed and minimal disk utilization.

## 🛠️ Technical Standards & Coding Tricks

### 1. SQL File Structure & Schema Versioning
- Every database migration or schema modification file must follow strict naming and ordering (e.g. `0001_init.sql`, `0002_add_compression.sql`).
- Maintain a single source of truth for the active schema inside the target microservice repository.

### 2. Design Patterns & Conventions
- **Naming Prefixes**:
  - Raw time-series tables: prefix with `ts_` (e.g. `ts_ticks`, `ts_trades`).
  - Continuous aggregates: prefix with `cagg_` (e.g. `cagg_ohlcv_1m`, `cagg_ohlcv_5m`).
  - Standard relational tables: prefix with `tbl_` (e.g. `tbl_symbols`, `tbl_exchanges`).
- **Facade Pattern (Views)**: Expose public database access through unified relational database Views or Functions rather than letting application engines run raw table scans.

### 3. Unified Comment Standards
- **Triple-Block Header**: Every `.sql` migration file MUST start with the standard header block:
  ```sql
  /*
   * ESSENTIAL PROCESS:
   * [Description of WHAT this SQL file does and WHY it exists]
   *
   * DATA FLOW:
   * 1. [Step 1]
   * 2. [Step 2]
   *
   * KEY PARAMETERS:
   * - [chunk_time_interval]: [interval duration]
   */
  ```
- **Empty Line Rule**: There must be exactly one empty line between the closing `*/` of the triple-block comment and the first line of code/SQL statements.
- **Horizontal Dividers**: Separate distinct logical blocks (e.g. table creations, indices, triggers) with exactly 77 dashes:
  `-- -----------------------------------------------------------------------------`

### 4. TimescaleDB Optimization Tricks (MANDATORY)
- **Hypertables**: Choose appropriate chunk intervals via `create_hypertable(..., chunk_time_interval => ...)` (e.g., `1 day` for ticks/high-frequency data, `7 days` for hourly data) ensuring that active chunks fit entirely within database RAM.
- **Index Optimization**: Use compound indexes on `(symbol, time DESC)` instead of standalone indices. Avoid indexing fields with low cardinality unless grouped.
- **Compression Policies**: Always enable Timescale compression policies for tables containing historical data:
  ```sql
  ALTER TABLE ts_ticks SET (timescaledb.compress, timescaledb.compress_segmentby = 'symbol');
  SELECT add_compression_policy('ts_ticks', INTERVAL '7 days');
  ```
- **Continuous Aggregates**: Use continuous aggregates for real-time OHLCV calculations. Use `add_real_time_aggregate_policy` to maintain auto-refresh loops.

### 5. Error & State Safeguards
- Write all migrations idempotently using `CREATE TABLE IF NOT EXISTS`, `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`, and `DROP TRIGGER IF EXISTS` blocks to prevent deployment script failures.

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**; since you have the code and logic, you MUST write both the implementation and its tests.
- **Scenarios**: For every schema modification, write/update Gherkin scenarios in `02-Business-BDD` to maintain BDD compliance.
- **Unit Tests**: Use `pgTAP` or SQL validation scripts to assert correct table partitions, indices, and view structures before handing over to the Lead Developer.

---
*Reference: [[Global-Architecture-Rules]], [[07-Configuration-Standard]]*
