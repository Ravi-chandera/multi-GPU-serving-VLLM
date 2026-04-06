# Phase 1 Findings - Baseline

## Goal

Measure how a single-GPU `vLLM` deployment performs before applying more advanced optimizations.

## Step-by-step analysis checklist

1. Record the exact GPU model and VRAM size.
2. Record the model name, precision, and max context length.
3. Paste the command used to start the server.
4. Copy the most important numbers from `results.csv`.
5. Note whether latency grows sharply as concurrency increases.
6. Note whether GPU memory, not compute, appears to be the first bottleneck.
7. Write one clear sentence describing the baseline you will compare against later phases.

## Server command used

Add your command here.

## Key observations

- Observation 1:
- Observation 2:
- Observation 3:

## Interpretation

Write why the baseline behaved the way it did.

## Next step

State what you expect to improve or worsen in the parallelism phase.
