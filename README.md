# AllBots.com.ai

**AI Brain Kits** for the AllBots ecosystem — modular intelligence modules that can be plugged into any bot, any repository.

A connection hub linking [AllBots.com](https://allbots.com), [Factory.ai](https://github.com/lippytm/Factory.ai), and all of [@lippytm](https://github.com/lippytm)'s repositories with a shared set of AI brain components.

---

## What are AI Brain Kits?

AI Brain Kits are drop-in intelligence bundles made up of four specialised brain modules:

| Module | Responsibility |
|---|---|
| `LanguageBrain` | Intent classification, sentiment analysis, text summarisation, response generation |
| `MemoryBrain` | Short-term conversation history + persistent long-term fact storage |
| `DecisionBrain` | Rule-aware option ranking and action selection |
| `LearningBrain` | Interaction logging, pattern analysis, and improvement recommendations |

Three pre-assembled kits are available to match any use-case:

| Kit | Brains included | Best for |
|---|---|---|
| **Starter** | Language + Memory | Quick prototypes, simple chatbots |
| **Standard** | Language + Memory + Decision | Business bots, workflow automation |
| **Full Stack** | All four brains | Production bots requiring self-improvement |

---

## Repository Structure

```
AllBots.com.ai/
│
├── brain/                    # Individual brain modules
│   ├── base_brain.py         # Abstract base (OpenAI client, retry logic)
│   ├── language_brain.py     # NLP: classify, sentiment, summarise, generate
│   ├── memory_brain.py       # Short-term + long-term memory
│   ├── decision_brain.py     # Option ranking and action selection
│   └── learning_brain.py     # Interaction logging and adaptive learning
│
├── kits/                     # Pre-assembled brain kits
│   ├── starter_kit.py        # Language + Memory
│   ├── standard_kit.py       # Language + Memory + Decision
│   └── full_stack_kit.py     # All four brains
│
├── config/
│   └── brain_config.yaml     # Kit & deployment configuration
│
├── .github/workflows/
│   ├── validate_brain_kits.yml   # CI: lint + test on every push/PR
│   └── deploy_brain_kits.yml     # Manual deploy to target repositories
│
├── deploy.py                 # CLI for deploying kits to repositories
├── requirements.txt
└── .gitignore
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your OpenAI API key

```bash
export OPENAI_API_KEY="sk-..."
```

Or add `OPENAI_API_KEY` to your repository's **Settings → Secrets and variables → Actions**.

### 3. Use a kit in your code

```python
from kits import StarterKit, StandardKit, FullStackKit

# ── Starter Kit ────────────────────────────────────────
kit = StarterKit()
reply = kit.chat("Hello! What can you do?")
print(reply)

# ── Standard Kit ───────────────────────────────────────
kit = StandardKit()
result = kit.run({
    "message": "I need help with my order",
    "goal": "resolve customer issue",
    "options": ["escalate", "refund", "provide info"],
})
print(result["reply"])

# ── Full Stack Kit ─────────────────────────────────────
kit = FullStackKit()
result = kit.run({"message": "What's the status of ticket #42?"})
print(result["reply"])

# Get learning insights after interactions:
insights = kit.get_insights()
recommendations = kit.get_recommendations()
```

### 4. Deploy to all repositories

```bash
# Deploy the standard kit to all configured targets
python deploy.py --kit standard

# Deploy the full stack kit to one specific repository
python deploy.py --kit full_stack --target lippytm/Factory.ai
```

Or trigger the **Deploy Brain Kits** workflow manually from the **Actions** tab.

---

## Configuration

Edit `config/brain_config.yaml` to adjust:

- **OpenAI model** and generation parameters
- **Active kit** (starter / standard / full_stack)
- **Memory** store path and short-term window size
- **Learning** log path and analysis limits
- **Target repositories** for deployment

---

## CI/CD Workflows

| Workflow | File | Trigger |
|---|---|---|
| Validate Brain Kits | `.github/workflows/validate_brain_kits.yml` | Push / PR touching `brain/`, `kits/`, `config/` |
| Deploy Brain Kits | `.github/workflows/deploy_brain_kits.yml` | Manual (`workflow_dispatch`) |

---

## Connected Repositories

These repositories are configured as brain kit deployment targets:

- [Factory.ai](https://github.com/lippytm/Factory.ai) — bot creation factory
- [Chatlippytm.ai.Bots](https://github.com/lippytm/Chatlippytm.ai.Bots) — AI hub with agent swarms
- [lippytm.ai](https://github.com/lippytm/lippytm.ai) — personal AI hub
- [Web3AI](https://github.com/lippytm/Web3AI) — Web3 AI integrations
- [AI-Time-Machines](https://github.com/lippytm/AI-Time-Machines) — AI automation
- And [all other lippytm repositories](https://github.com/lippytm) listed in `config/brain_config.yaml`
