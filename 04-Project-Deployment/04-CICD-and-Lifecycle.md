---
title: CI/CD and Lifecycle
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📐 CI/CD and Lifecycle

### 🏛️ Definition Layer
This document defines the high-level architectural requirements for the platform's lifecycle. For stage-by-stage implementation protocols, see **[[05-Fleet-Operation/05-Fleet-Strategy/02-CI-Protocols|📡 Fleet CI Protocols]]**.

## Architectural Rule
All microservices MUST be containerized and published to the **GitHub Container Registry (GHCR)**. Deployment is managed via `docker-compose` with `Watchtower` providing automated continuous delivery for non-critical services.

## Motivation (Why?)
- **Immutable Infrastructure**: Ensures the exact same binary tested in the sandbox is deployed to production.
- **Automated Delivery**: Reduces manual intervention and human error during deployment cycles.

## 🔄 Deployment & Rollback
- **Continuous Delivery**: `Watchtower` monitors GHCR for new images and triggers rolling updates.
- **Selective Updates**: To prevent data corruption, stateful services (Databases, Config Server) MUST disable auto-updates via the `com.centurylinklabs.watchtower.enable=false` label.
- **Rollback**: To revert a service, update the `TAG` variable in the `.env.develop` or `.env.main` file to a previous stable version and execute `docker compose up -d`.

## 🚀 Image Promotion Gate
We utilize a multi-stage promotion flow to ensure fleet stability:

1.  **`develop` Branch**: Every push triggers a build and publishes to the `latest` tag (or `develop` tag).
2.  **Sandbox Validation**: The **`sandbox-testing`** environment automatically pulls the new `latest` images and runs all functional/resilience scenarios.
3.  **`main` Branch Merge**: Upon successful sandbox validation and manual sign-off, code is merged into `main`.
4.  **Semantic Tagging**: Merges to `main` (or specific Git Tags) trigger the publication of a pinned version (e.g., `v1.2.3`).
5.  **Production Release**: The production `docker-deployment` is updated to point its `TAG` variable to the new pinned version.

## 🔐 Registry Authentication
CI/CD workflows utilize the `GITHUB_TOKEN` (or a dedicated `REGISTRY_TOKEN`) with `packages:write` permissions to authenticate with `ghcr.io`. Local deployment environments must be authenticated via `docker login ghcr.io`.
