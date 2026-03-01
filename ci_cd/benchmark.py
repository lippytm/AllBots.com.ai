#!/usr/bin/env python3
"""
ci_cd/benchmark.py
==================
Dynamic intelligence benchmarking script.

Runs each registered bot against a standard task suite, measures latency and
output quality, and writes a JSON report to ``benchmark_results.json``.

Usage
-----
    python ci_cd/benchmark.py
"""
from __future__ import annotations

import json
import time
import sys

from bots import ResearchBot


BENCHMARK_TASKS = [
    "What are the latest advances in swarm robotics?",
    "Summarise recent Web3 governance proposals.",
    "List multicloud cost-optimisation strategies.",
]


def benchmark_bot(bot, tasks: list[str]) -> list[dict]:
    results = []
    for task in tasks:
        start = time.perf_counter()
        output = bot.run(task)
        elapsed = time.perf_counter() - start
        results.append({"task": task, "latency_s": round(elapsed, 6), "output": output})
    return results


def main() -> int:
    print("=" * 60)
    print("AllBots.com.ai — Intelligence Benchmark")
    print("=" * 60)

    report = {}

    research_bot = ResearchBot(sources=["https://arxiv.org", "https://scholar.google.com"])
    report["ResearchBot"] = benchmark_bot(research_bot, BENCHMARK_TASKS)

    output_path = "benchmark_results.json"
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    print(f"\n📊  Benchmark complete. Results written to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
