---
title: "Environment Variables"
type: architecture
status: active
microservice: ecosystem-wide
---

# 📐 Environment Variables

## Architectural Rule
Production secrets and configuration are injected via environment variables. Values in YAML files use `${VAR_NAME}` syntax for expansion at runtime.

## Motivation (Why?)
- Security: Keeps secrets out of source code.
- Portability: Allows the same container image to run in different environments by changing variables.

## Examples
- `DB_PASSWORD` — Database credentials.
- `NATS_IP`, `NATS_PORT` — NATS connectivity.
- `ENV_PROD` — Production environment flag.
- `TAG` — Docker image tag (default: `latest`).
