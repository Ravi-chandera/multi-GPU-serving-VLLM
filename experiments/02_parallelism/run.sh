#!/usr/bin/env bash

# Phase 2: Tensor parallelism vs alternative multi-GPU serving layouts
#
# Step 1: choose the configuration you want to test.
# Step 2: adjust MODEL_PATH, GPU count assumptions, and MODEL_NAME labels.
# Step 3: start the server with the selected parallelism settings.
# Step 4: run the benchmark for each configuration and append all rows to results.csv.
# Step 5: compare throughput and latency against the baseline phase.

MODEL_PATH="../../models/llama-8b"
HOST="127.0.0.1"
PORT="8000"
REQUESTS="100"
CONCURRENCY="16"
INPUT_TOKENS="512"
OUTPUT_TOKENS="128"
RESULTS_FILE="results.csv"

# Step 6: Example A - tensor parallelism across 2 GPUs.
# python -m vllm.entrypoints.openai.api_server #   --model "${MODEL_PATH}" #   --served-model-name "llama-8b-tp2" #   --tensor-parallel-size 2 #   --host "${HOST}" #   --port "${PORT}"
# python ../../benchmarks/benchmark_serving.py #   --host "${HOST}" #   --port "${PORT}" #   --model "llama-8b-tp2" #   --requests "${REQUESTS}" #   --concurrency "${CONCURRENCY}" #   --input-tokens "${INPUT_TOKENS}" #   --output-tokens "${OUTPUT_TOKENS}" #   --label "tensor_parallel_2" #   --output "${RESULTS_FILE}" #   --append

# Step 7: Example B - tensor parallelism across 4 GPUs.
# Repeat the same process with a different served model name and tensor parallel size.

# Step 8: If you want to approximate pipeline-style deployment, run two independent server replicas
# behind a load balancer and benchmark the balanced endpoint separately.

# Step 9: This file is intentionally a template, so uncomment only the block you are actively testing.
