# Phase 3 Findings - KV Cache Stress Test

## Goal

Understand how prompt length and concurrent generation load affect memory usage and tail latency.

## Step-by-step analysis checklist

1. Record the fixed server configuration used for this phase.
2. Note which variable you changed in each run: input tokens, output tokens, or concurrency.
3. Identify the first configuration where performance degrades sharply.
4. Compare average latency with p95 and p99 latency.
5. Note any failed requests or server-side warnings.
6. Explain whether the bottleneck looks memory-bound, scheduler-bound, or both.
7. Summarize the safe operating region for this model on your hardware.

## Stress conditions tested

- Condition 1:
- Condition 2:
- Condition 3:

## Key observations

- Observation 1:
- Observation 2:
- Observation 3:

## Interpretation

Describe how KV cache growth changed the system behavior.

## Next step

State whether quantization might help by reducing memory pressure in the next phase.
