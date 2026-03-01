#!/usr/bin/env bash
# validate_connections.sh — verifies that config/connections.json is well-formed
set -euo pipefail

CONFIG_FILE="$(dirname "$0")/../config/connections.json"

echo "Validating $CONFIG_FILE ..."

if command -v python3 &>/dev/null; then
  python3 - "$CONFIG_FILE" <<'PY'
import json, sys
cfg_path = sys.argv[1]
with open(cfg_path) as f:
    data = json.load(f)
projects = data.get('projects', {})
if not projects:
    print('ERROR: no projects found in connections.json', file=sys.stderr)
    sys.exit(1)
for key, proj in projects.items():
    for field in ('name', 'url', 'description', 'platform'):
        if field not in proj:
            print(f'ERROR: project "{key}" missing field "{field}"', file=sys.stderr)
            sys.exit(1)
print(f'OK — {len(projects)} project(s) validated.')
PY
else
  echo "python3 not found — skipping validation"
fi
