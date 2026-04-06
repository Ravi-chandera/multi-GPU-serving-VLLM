# Phase 2 Findings - Parallelism

## Goal

Compare whether adding GPUs improves throughput enough to justify the coordination overhead.

## Step-by-step analysis checklist

1. List every tested parallel configuration.
2. Record the GPU count used by each configuration.
3. Note whether throughput scaled linearly, sub-linearly, or not at all.
4. Note whether latency improved, stayed flat, or worsened.
5. Record any signs of communication overhead.
6. Compare the best result against the single-GPU baseline.
7. State which configuration you would keep for production and why.

## Configurations tested

- Configuration 1:
- Configuration 2:
- Configuration 3:

## Key observations

- Observation 1:
- Observation 2:
- Observation 3:

## Interpretation

Explain whether parallelism helped mainly with memory fitting, throughput, or both.

## Next step

State what you expect the KV cache phase to reveal about long prompts and concurrency.
