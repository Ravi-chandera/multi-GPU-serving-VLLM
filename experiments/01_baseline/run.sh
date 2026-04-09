#!/bin/bash

# Ensure environment is active
source /workspace/venv/bin/activate

# Launch vLLM
vllm serve NousResearch/Hermes-3-Llama-3.1-8B \
    --dtype float16 \
    --max-model-len 8192