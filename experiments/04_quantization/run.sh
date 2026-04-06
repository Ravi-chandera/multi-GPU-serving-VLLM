#!/usr/bin/env bash

# Phase 4: Quantization comparison
#
# Step 1: prepare separate model variants or launch flags for FP16, INT8, and INT4.
# Step 2: serve one precision format at a time.
# Step 3: keep prompt sizes and concurrency as constant as possible for fair comparison.
# Step 4: append benchmark results for each precision to results.csv.
# Step 5: note both speed changes and quality trade-offs outside this table if you observe them.

HOST="127.0.0.1"
PORT="8000"
REQUESTS="100"
CONCURRENCY="8"
INPUT_TOKENS="512"
OUTPUT_TOKENS="128"
RESULTS_FILE="results.csv"

# Step 6: Example FP16 benchmark after serving the FP16 model.
# python ../../benchmarks/benchmark_serving.py #   --host "${HOST}" #   --port "${PORT}" #   --model "llama-8b-fp16" #   --requests "${REQUESTS}" #   --concurrency "${CONCURRENCY}" #   --input-tokens "${INPUT_TOKENS}" #   --output-tokens "${OUTPUT_TOKENS}" #   --label "fp16" #   --output "${RESULTS_FILE}" #   --append

# Step 7: Example INT8 benchmark.
# Repeat after serving the INT8 configuration.

# Step 8: Example INT4 benchmark.
# Repeat after serving the INT4 configuration.

# Step 9: keep notes about memory savings, throughput gains, and any noticeable output quality changes.
