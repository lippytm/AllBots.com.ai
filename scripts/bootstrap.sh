#!/usr/bin/env bash
# bootstrap.sh — sets up the local development environment for AllBots.com.ai
set -euo pipefail

CONFIG_FILE="$(dirname "$0")/../config/connections.json"

echo "=== AllBots.com.ai Bootstrap ==="

# Validate JSON config
if command -v python3 &>/dev/null; then
  python3 - "$CONFIG_FILE" <<'PY'
import json, sys
cfg_path = sys.argv[1]
with open(cfg_path) as f:
    json.load(f)
print('✅  config/connections.json is valid JSON')
PY
elif command -v node &>/dev/null; then
  node - "$CONFIG_FILE" <<'JS'
const fs = require('fs');
JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
console.log('✅  config/connections.json is valid JSON');
JS
else
  echo "⚠️  Neither python3 nor node found — skipping JSON validation"
fi

# List connected projects
echo ""
echo "Connected projects:"
if command -v python3 &>/dev/null; then
  python3 - "$CONFIG_FILE" <<'PY'
import json, sys
cfg = json.loads(open(sys.argv[1]).read())
for k, v in cfg.get("projects", {}).items():
    print(f"  • {v['name']}: {v['url']}")
PY
fi

echo ""
echo "Bootstrap complete. See CONNECTIONS.md for full integration details."
