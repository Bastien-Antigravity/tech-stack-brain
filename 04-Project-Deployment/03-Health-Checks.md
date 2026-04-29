---
title: "Health Checks"
type: architecture
status: active
microservice: ecosystem-wide
---

# 📐 Health Checks

## Architectural Rule
Every core service must provide a mechanism for health monitoring. 

## Motivation (Why?)
- High availability: Allows orchestrators (Docker Compose, Kubernetes) to restart unhealthy containers.
- Dependency management: Ensuring the database is ready before the application starts.

## Examples
- **TimescaleDB**: Uses `pg_isready` to verify database readiness.
- **NATS**: Monitors the HTTP monitoring endpoint on port 8222.
- **Application Services**: Implement `grpc_health_v1` for gRPC health checks with `SERVING` status.
