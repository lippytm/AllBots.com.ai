# Cross-Project Connections

This document is the living registry of every external repository and platform that **AllBots.com.ai** integrates with. Update this file whenever a new connection is established or an existing one changes.

---

## Core Ecosystem

| Repository | URL | Role |
|------------|-----|------|
| **AllBots.com** | <https://github.com/lippytm/AllBots.com> | Bot management and GitHub automation hub |
| **Factory.ai** | <https://github.com/lippytm/Factory.ai> | Workflow orchestration connecting GitHub, ChatGPT, and AllBots.com |
| **lippytm.ai** | <https://github.com/lippytm/lippytm.ai> | AI Web3 connection hub (Gist, GitLab, GitHub) |

## AI & Intelligence Engines

| Repository | URL | Role |
|------------|-----|------|
| **Web3AI** | <https://github.com/lippytm/Web3AI> | Web3 + AI integration layer |
| **Chatlippytm.ai.Bots** | <https://github.com/lippytm/Chatlippytm.ai.Bots> | ManyChat / BotBuilders business-of-businesses hub |
| **OpenClaw-lippytm.AI-** | <https://github.com/lippytm/OpenClaw-lippytm.AI-> | Personal AI assistant creation & networking platform |
| **AI-Full-Stack-AI-DevOps-…** | <https://github.com/lippytm/AI-Full-Stack-AI-DevOps-Synthetic-Intelligence-Engines-AgentsBots-Web3-Websites-> | Full-stack AI/DevOps + Web3 websites |

## Automation & Time Machines

| Repository | URL | Role |
|------------|-----|------|
| **AI-Time-Machines** | <https://github.com/lippytm/AI-Time-Machines> | AI agents + time-machine automation |
| **Time-Machines-Builders-** | <https://github.com/lippytm/Time-Machines-Builders-> | Learn-to-code AI automation & blockchain development |
| **Transparency-Logic-Time-Machine-Bots-** | <https://github.com/lippytm/Transparency-Logic-Time-Machine-Bots-> | Grand United Fields of Theories (TypeScript) |

---

## Integration Patterns

### 1 — Shared Configuration
All connected projects should reference `config/connections.json` in **AllBots.com.ai** for canonical API endpoint and service-registry values.

### 2 — CI Synchronization
The `.github/workflows/ci.yml` pipeline in this repo validates that `config/connections.json` is well-formed and that all listed URLs are reachable.

### 3 — Script Reuse
Common bootstrap and utility scripts live in `scripts/`. Copy or submodule them into any connected repository rather than duplicating logic.

---

## Adding a New Connection

1. Add the repository to the correct table above.
2. Add any new API base URLs to `config/connections.json`.
3. Open a Pull Request and tag it with the `connection` label.
