#!/bin/bash

# 1. Create folders
mkdir -p /workspace/hf_cache /workspace/tmp /workspace/venv /workspace/uv_cache

# 2. Set env vars in .bashrc (only if they aren't already there)
# Use 'grep' to check for existing entries before appending
VAR_ENTRIES=(
    'export HF_HOME=/workspace/hf_cache'
    'export TMPDIR=/workspace/tmp'
    'export UV_CACHE_DIR=/workspace/uv_cache'
    'export UV_NO_CACHE=1'
    'source /workspace/venv/bin/activate'
)

for entry in "${VAR_ENTRIES[@]}"; do
    if ! grep -qF "$entry" ~/.bashrc; then
        echo "$entry" >> ~/.bashrc
        echo "Added: $entry"
    fi
done

# 3. Install uv
pip install uv

# 4. Create venv and install vllm
uv venv /workspace/venv
source /workspace/venv/bin/activate
uv pip install vllm --no-cache

echo "Setup complete. Run you LLMs."