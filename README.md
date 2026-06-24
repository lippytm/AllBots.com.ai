# AllBots.com.ai

A cross-project, cross-platform hub connecting **AllBots.com** with **Factory.ai** and the broader lippytm ecosystem.

## Overview

AllBots.com.ai serves as the integration layer that bridges AI bot management, automation workflows, and multi-platform development. It provides shared configuration, reusable scripts, and documented connection patterns so every linked project can interoperate smoothly.

## Repository Map

| Directory | Purpose |
|-----------|---------|
| `config/` | Cross-platform connection configurations (API endpoints, service registries) |
| `scripts/` | Shared automation and bootstrap scripts |
| `docs/` | Architecture diagrams, onboarding guides, integration patterns |
| `.github/workflows/` | CI/CD pipelines for validation and deployment |

## Connected Projects

See [CONNECTIONS.md](./CONNECTIONS.md) for the full registry of linked repositories and integration notes.

## Quick Start

```bash
# Clone and enter the repo
git clone https://github.com/lippytm/AllBots.com.ai.git
cd AllBots.com.ai

# Review connection config
cat config/connections.json

# Run the bootstrap helper
bash scripts/bootstrap.sh
```

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-change`).
3. Commit your changes and open a Pull Request.

## License

MIT

