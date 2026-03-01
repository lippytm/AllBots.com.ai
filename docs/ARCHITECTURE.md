# Architecture Overview

## AllBots.com.ai — Integration Hub

```
┌────────────────────────────────────────────────────────┐
│                   AllBots.com.ai                       │
│              (cross-project hub)                       │
│                                                        │
│  config/connections.json  ──► service registry         │
│  scripts/bootstrap.sh     ──► local dev setup          │
│  scripts/validate_connections.sh ──► CI validation     │
│  .github/workflows/ci.yml ──► automated checks         │
└──────────┬─────────────────────┬──────────────────────┘
           │                     │
    ┌──────▼──────┐       ┌──────▼──────┐
    │ AllBots.com │       │ Factory.ai  │
    │ (bot mgmt)  │       │ (workflows) │
    └──────┬──────┘       └──────┬──────┘
           │                     │
    ┌──────▼──────────────────────▼──────┐
    │          lippytm Ecosystem         │
    │  Web3AI · Chatlippytm.ai.Bots      │
    │  AI-Time-Machines · lippytm.ai     │
    │  OpenClaw · AI-Full-Stack …        │
    └────────────────────────────────────┘
```

## Key Concepts

### Service Registry (`config/connections.json`)
A single source of truth for every connected repository and its metadata. Any project in the ecosystem can read this file to discover peers and their API base URLs.

### Bootstrap Script (`scripts/bootstrap.sh`)
Validates the local environment and prints a summary of all connected projects. Run it after cloning to confirm everything is wired up correctly.

### CI Pipeline (`.github/workflows/ci.yml`)
Runs on every push/PR to `main` to ensure `connections.json` stays valid and all shell scripts are lint-clean.

## Adding a New Platform Integration

1. Add the platform to `config/connections.json` under `"platforms"`.
2. Reference it from each project's `"platform"` field.
3. Update `CONNECTIONS.md` and this document.
4. The CI pipeline will validate the new entry automatically.
