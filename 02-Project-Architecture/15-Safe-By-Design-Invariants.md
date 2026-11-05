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
- '#service/ecosystem-wide'
---
# 15. Safe-by-Design Invariants & Concurrency Invariant Ledger
*Generated: 2026-11-05 12:26:43 UTC | Target: `/Users/imac/Desktop/Bastien-Antigravity/obsidian-brain/08-Squad-Agent`*

> [!IMPORTANT]
> This ledger establishes what is **formally safe by design** without locks, mutexes, or defensive double-checking.
> AI agents and developers must consult this matrix before adding concurrency primitives or redundant validation.

## 📊 Summary of Invariants
- **Level 1 (Memory & Primitives)**: 54 verified atomic / immutable structures.
- **Level 2 (Runtime Concurrency)**: 85 verified channel-transferred / asyncio-cooperative workflows.
- **Level 3 (Component Boundaries)**: Verified package encapsulation with zero 1-to-1 interface bloat.
- **Level 4 (Fleet & Transports)**: Wire-format & database constraint guarantees.

## 🔬 Level 1: Hardware & Memory Primitives (Zero Mutex Required)
| File | Line | Identifier | Architecture Reason |
| :--- | :--- | :--- | :--- |
| `main.py` | L31 | `COMMANDS_MAP` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `test_fleet_version.py` | L18 | `SQUAD_AGENT_DIR` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `test_scaffold_brain.py` | L25 | `SQUAD_AGENT_DIR` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `test_ecosystem_compliance.py` | L25 | `SQUAD_AGENT_DIR` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `test_scaffold_integration.py` | L25 | `SQUAD_AGENT_DIR` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `test_scaffold_microservice.py` | L22 | `SQUAD_AGENT_DIR` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `discord_client.py` | L25 | `HAS_DISCORD` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `discord_client.py` | L28 | `HAS_DISCORD` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `agent_dispatcher.py` | L41 | `WORKSPACE_ROOT` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `agent_dispatcher.py` | L42 | `OBSIDIAN_DIR` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `agent_dispatcher.py` | L47 | `ROLE_PROMPT_SOURCES` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `agent_dispatcher.py` | L52 | `ROLE_MAP` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `agent_dispatcher.py` | L93 | `SEMANTIC_KEYWORDS` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `start_squad.py` | L87 | `C_RESET` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `start_squad.py` | L88 | `C_GREEN` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `start_squad.py` | L89 | `C_RED` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `start_squad.py` | L90 | `C_BOLD` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `start_squad.py` | L520 | `EXCLUSIONS` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `switch_mode.py` | L38 | `MODES` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `server.py` | L49 | `_STATIC_DIR` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `base_agent.py` | L355 | `MAX_TOOL_TURNS` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `squad_control_pb2.py` | L27 | `DESCRIPTOR` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `squad_control_pb2_grpc.py` | L8 | `GRPC_GENERATED_VERSION` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `squad_control_pb2_grpc.py` | L9 | `GRPC_VERSION` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |
| `pg_pool.py` | L27 | `HAS_POSTGRES` | Module-level constant initialized at load time. Thread-safe for read-only access without locks. |

## ⚡ Level 2: Runtime Concurrency Models (CSP & Cooperative Scheduling)
| File | Line | Identifier | Concurrency Model Reason |
| :--- | :--- | :--- | :--- |
| `test_chat_endpoints.py` | L128 | `async def test_publish_and_get_history_without_postgres()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L44 | `async def test_pub_sub_direct()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L46 | `async def cb()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L57 | `async def test_tag_routing_orchestrator_mention()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L59 | `async def orchestrator_cb()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L77 | `async def test_tag_routing_fallback_orchestrator()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L79 | `async def orchestrator_cb()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L97 | `async def test_cross_brain_tag_routing_satellite_to_root()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L99 | `async def root_dev_cb()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L119 | `async def test_cross_brain_tag_routing_root_to_satellite()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L121 | `async def satellite_trader_cb()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L140 | `async def test_cross_brain_isolation_intra_brain_no_crosstalk()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L144 | `async def root_cb()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L147 | `async def analyst_cb()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L174 | `async def test_connect_success()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L187 | `async def test_connect_offline_fallback()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L197 | `async def test_connect_offline_fail_fast_enforcement()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L206 | `async def test_publish_fail_fast_when_offline()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_event_bus.py` | L215 | `async def test_config_legacy_string_compatibility()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_strategic_nexus_articulation.py` | L74 | `async def test_oracle_check_anti_backlog_hit()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_strategic_nexus_articulation.py` | L91 | `async def test_oracle_check_anti_backlog_clean()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_strategic_nexus_articulation.py` | L103 | `async def test_oracle_record_strategic_milestone()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `test_strategic_nexus_articulation.py` | L132 | `async def test_orchestrator_record_strategic_milestone()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `discord_client.py` | L83 | `async def _stream_squad_events_to_discord()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |
| `discord_client.py` | L101 | `async def squad_event_callback()` | Runs on single-threaded event loop. Pure synchronous statements are atomic relative to other coroutines. |

## 🌐 Level 4: Fleet & Network Boundary Invariants
- **Wire Serialization**: Cap'n Proto / Protobuf ensure strict byte-level type guarantees at socket ingress.
- **Database Engine**: PostgreSQL `obsidiandb` handles uniqueness via unique indexes & `ON CONFLICT`.
- **Transport Mesh**: SafeSocket & NATS maintain auto-reconnection pools; manual retry loops are prohibited.
