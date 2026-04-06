#!/usr/bin/env python3
"""Create a throughput comparison chart across all experiment result files.

Step-by-step usage:
1. Fill in each experiment results.csv with benchmark rows.
2. Run this script from the project root or by using its full path.
3. It will read all phase CSV files, skip comment lines, and collect valid rows.
4. It will save a bar chart image to charts/throughput_comparison.png by default.
5. Use the chart inside your final write-up.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


DEFAULT_FILES = [
    Path("../experiments/01_baseline/results.csv"),
    Path("../experiments/02_parallelism/results.csv"),
    Path("../experiments/03_kv_cache/results.csv"),
    Path("../experiments/04_quantization/results.csv"),
]


def read_results(csv_path: Path) -> list[dict]:
    """Read one CSV file while skipping comment lines."""
    if not csv_path.exists():
        return []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        filtered_lines = [line for line in handle if line.strip() and not line.lstrip().startswith("#")]
    if not filtered_lines:
        return []
    reader = csv.DictReader(filtered_lines)
    rows = []
    for row in reader:
        if row.get("label") and row.get("throughput_rps"):
            rows.append(row)
    return rows


def collect_all_rows(script_dir: Path) -> list[dict]:
    """Collect rows from all default result files."""
    rows: list[dict] = []
    for relative_path in DEFAULT_FILES:
        rows.extend(read_results((script_dir / relative_path).resolve()))
    return rows


def make_chart(rows: list[dict], output_path: Path) -> None:
    """Create a bar chart from result rows."""
    if not rows:
        raise ValueError("No benchmark rows were found. Populate the experiment CSV files first.")
    labels = [row["label"] for row in rows]
    throughput_values = [float(row["throughput_rps"]) for row in rows]
    plt.figure(figsize=(12, 6))
    bars = plt.bar(labels, throughput_values)
    plt.title("LLM Serving Throughput Comparison")
    plt.xlabel("Configuration")
    plt.ylabel("Throughput (requests per second)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    for bar, value in zip(bars, throughput_values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{value:.2f}", ha="center", va="bottom")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150)
    print(f"Saved chart to {output_path}")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for chart generation."""
    parser = argparse.ArgumentParser(description="Create a throughput comparison chart.")
    parser.add_argument("--output", type=Path, default=Path("throughput_comparison.png"), help="Path to the output PNG file.")
    return parser.parse_args()


def main() -> None:
    """Run chart generation."""
    args = parse_args()
    script_dir = Path(__file__).resolve().parent
    output_path = args.output
    if not output_path.is_absolute():
        output_path = (script_dir / output_path).resolve()
    rows = collect_all_rows(script_dir)
    make_chart(rows, output_path)


if __name__ == "__main__":
    main()
