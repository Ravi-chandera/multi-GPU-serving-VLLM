# LLM Inference at Scale

This project is a hands-on scaffold for studying how `vLLM` behaves when you serve a model under different inference configurations.

## What this project covers

1. **Baseline**: Measure single-GPU serving throughput and latency.
2. **Parallelism**: Compare tensor parallelism and pipeline-style deployment choices.
3. **KV cache**: Stress long-context and concurrency to observe memory pressure.
4. **Quantization**: Compare FP16, INT8, and INT4 style deployments.

## Project layout

- `models/llama-8b/` -> place the downloaded model here.
- `experiments/` -> run scripts, raw result tables, and notes for each phase.
- `benchmarks/benchmark_serving.py` -> lightweight benchmark client for an OpenAI-compatible vLLM server.
- `charts/throughput_comparison.py` -> combines experiment CSV files into one comparison chart.
- `writeup.md` -> short narrative template for your final summary.

## Step-by-step setup

1. Install Python and create a virtual environment.
2. Install required packages such as `vllm`, `matplotlib`, and any quantization dependencies you plan to test.
3. Download your model into `models/llama-8b/`.
4. Start a vLLM server for the configuration you want to test.
5. Run the matching experiment `run.sh` file after updating paths and parameters.
6. Store numeric results in the matching `results.csv` file.
7. Write observations in the matching `findings.md` file.
8. Generate the final chart with `charts/throughput_comparison.py`.
9. Summarize the overall story in `writeup.md`.

## Model download example

Use a command like the one below after logging into Hugging Face and accepting the model license if needed.

- Step 1: install the Hugging Face CLI.
- Step 2: run `huggingface-cli login`.
- Step 3: download the model into `models/llama-8b/`.
- Step 4: confirm the tokenizer and weight files exist inside that directory.

Example command pattern:

`huggingface-cli download <model-repo> --local-dir models/llama-8b`

## Suggested Python packages

- `vllm`
- `matplotlib`
- `pandas` if you prefer richer analysis
- `bitsandbytes` if you test some quantized flows

## Notes on scope

The attached roadmap preview available in this chat only exposed styling markup in the visible snippet, so this scaffold is based on your requested directory structure and a standard vLLM evaluation workflow. If you want, I can refine the experiment assumptions after you share the roadmap text or a copy inside the project folder.
