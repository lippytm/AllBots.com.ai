"""Brain Kits deployment CLI.

Usage
-----
    python deploy.py --kit standard --target lippytm/AllBots.com

If ``--target`` is omitted, the kit is deployed to all repositories
listed in ``config/brain_config.yaml``.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import Any

import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("deploy")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "brain_config.yaml")


def load_config() -> dict[str, Any]:
    with open(CONFIG_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def deploy_to_repo(kit_name: str, repo: str) -> None:
    """Simulate deploying a brain kit to a repository.

    In a real deployment this function would use the GitHub API (or a
    sub-process) to push the selected kit files into *repo*.  For now
    it logs the action so the workflow output is meaningful.
    """
    logger.info("Deploying %-12s kit → %s", kit_name, repo)
    # Future: call GitHub API to create/update kit files in target repo.


def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy AI Brain Kits to repositories.")
    parser.add_argument(
        "--kit",
        choices=["starter", "standard", "full_stack"],
        default="standard",
        help="Brain kit to deploy",
    )
    parser.add_argument(
        "--target",
        default="",
        help="Target repository (owner/repo).  Omit to deploy to all targets.",
    )
    args = parser.parse_args()

    config = load_config()
    targets: list[str] = (
        [args.target]
        if args.target
        else config.get("repositories", {}).get("targets", [])
    )

    if not targets:
        logger.error("No target repositories configured or specified.")
        sys.exit(1)

    logger.info("Deploying '%s' kit to %d repository/ies …", args.kit, len(targets))
    for repo in targets:
        deploy_to_repo(args.kit, repo)

    logger.info("Deployment complete.")


if __name__ == "__main__":
    main()
