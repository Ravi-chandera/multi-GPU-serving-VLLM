#!/usr/bin/env bash

# Phase 3: KV cache stress test
#
# Step 1: keep the model and GPU setup fixed so this phase isolates KV cache effects.
# Step 2: vary input length, output length, or concurrency to increase cache pressure.
# Step 3: append one benchmark row per stress condition.
# Step 4: observe when latency spikes or requests begin to fail.
# Step 5: record any memory-related warnings from the vLLM server logs.

HOST="127.0.0.1"
PORT="8000"
MODEL_NAME="llama-8b-kv"
RESULTS_FILE="results.csv"

# Step 6: Example low-pressure run.
python ../../benchmarks/benchmark_serving.py   --host "${HOST}"   --port "${PORT}"   --model "${MODEL_NAME}"   --requests 50   --concurrency 4   --input-tokens 512   --output-tokens 128   --label "kv_low_pressure"   --output "${RESULTS_FILE}"   --append

# Step 7: Example medium-pressure run.
python ../../benchmarks/benchmark_serving.py   --host "${HOST}"   --port "${PORT}"   --model "${MODEL_NAME}"   --requests 50   --concurrency 8   --input-tokens 2048   --output-tokens 256   --label "kv_medium_pressure"   --output "${RESULTS_FILE}"   --append

# Step 8: Example high-pressure run.
python ../../benchmarks/benchmark_serving.py   --host "${HOST}"   --port "${PORT}"   --model "${MODEL_NAME}"   --requests 50   --concurrency 16   --input-tokens 4096   --output-tokens 512   --label "kv_high_pressure"   --output "${RESULTS_FILE}"   --append

# Step 9: increase only one variable at a time if you want cleaner causal conclusions.
