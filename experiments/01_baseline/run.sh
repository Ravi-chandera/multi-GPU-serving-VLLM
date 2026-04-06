#!/usr/bin/env bash

# Phase 1: Single GPU baseline benchmark
#
# Step 1: update MODEL_PATH so it points at your local model folder.
# Step 2: start the vLLM server in a separate terminal using a single GPU.
# Step 3: make sure the server is reachable at HOST:PORT below.
# Step 4: run this script to execute a benchmark and append the results.
# Step 5: review results.csv and findings.md after the run completes.

MODEL_PATH="../../models/llama-8b"
HOST="127.0.0.1"
PORT="8000"
MODEL_NAME="llama-8b-baseline"
REQUESTS="100"
CONCURRENCY="8"
INPUT_TOKENS="512"
OUTPUT_TOKENS="128"
RESULTS_FILE="results.csv"

# Step 6: example server command.
# Uncomment and run this in another terminal before benchmarking.
# python -m vllm.entrypoints.openai.api_server #   --model "${MODEL_PATH}" #   --served-model-name "${MODEL_NAME}" #   --host "${HOST}" #   --port "${PORT}"

# Step 7: run the benchmark client against the live server.
python ../../benchmarks/benchmark_serving.py   --host "${HOST}"   --port "${PORT}"   --model "${MODEL_NAME}"   --requests "${REQUESTS}"   --concurrency "${CONCURRENCY}"   --input-tokens "${INPUT_TOKENS}"   --output-tokens "${OUTPUT_TOKENS}"   --label "baseline_single_gpu"   --output "${RESULTS_FILE}"   --append

# Step 8: if you want more stable numbers, repeat the run 3 times and average later.
