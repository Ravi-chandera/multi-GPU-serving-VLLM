"""
vLLM Load Tester with Locust
============================
Usage:
  pip install locust

  # Headless mode (auto-runs, dumps CSV):
  locust -f vllm_loadtest.py --headless \
    -u 50 -r 10 \
    --run-time 2m \
    --csv=results/vllm_metrics \
    --host http://localhost:8000

  # UI mode (open browser at http://localhost:8089):
  locust -f vllm_loadtest.py --host http://localhost:8000

CSV files produced:
  results/vllm_metrics_stats.csv        <- per-endpoint stats
  results/vllm_metrics_stats_history.csv <- stats over time
  results/vllm_metrics_failures.csv     <- failed requests
"""

import json
import time
import csv
import os
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner, LocalRunner

# ─── CONFIG ──────────────────────────────────────────────────────────────────
MODEL_NAME   = "mistralai/Mistral-7B-Instruct-v0.2"   # change to your model
MAX_TOKENS   = 256
TEMPERATURE  = 0.7
RESULTS_DIR  = "results"

# Prompts pool — Locust picks one per request
PROMPTS = [
    "Explain the difference between supervised and unsupervised learning.",
    "What is the capital of France and what is it known for?",
    "Write a short poem about the night sky.",
    "Summarize the theory of relativity in 3 sentences.",
    "What are the benefits of drinking water regularly?",
    "Explain what an API is to a 10-year-old.",
    "List 5 tips for improving productivity.",
    "What is Python used for in data science?",
    "Describe how a neural network learns.",
    "What is the difference between RAM and storage?",
]
# ─────────────────────────────────────────────────────────────────────────────


# Custom per-request metrics collector
_custom_rows = []

def record_custom(name, prompt_tokens, latency_ms, ttft_ms, success):
    _custom_rows.append({
        "timestamp":     time.strftime("%Y-%m-%dT%H:%M:%S"),
        "request_name":  name,
        "prompt_tokens": prompt_tokens,
        "latency_ms":    round(latency_ms, 2),
        "ttft_ms":       round(ttft_ms, 2),
        "success":       success,
    })


class VLLMUser(HttpUser):
    """Simulates a user hitting the vLLM /v1/chat/completions endpoint."""
    wait_time = between(0.5, 2)   # seconds between requests per user

    @task
    def chat_completion(self):
        import random
        prompt = random.choice(PROMPTS)

        payload = {
            "model":       MODEL_NAME,
            "messages":    [{"role": "user", "content": prompt}],
            "max_tokens":  MAX_TOKENS,
            "temperature": TEMPERATURE,
        }

        t0 = time.perf_counter()
        with self.client.post(
            "/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            catch_response=True,
            name="POST /v1/chat/completions",
        ) as resp:
            latency_ms = (time.perf_counter() - t0) * 1000

            if resp.status_code == 200:
                try:
                    data          = resp.json()
                    prompt_tokens = data.get("usage", {}).get("prompt_tokens", 0)
                    # vLLM exposes TTFT in the response header (ms)
                    ttft_ms       = float(resp.headers.get("x-ttft-ms", latency_ms))
                    record_custom(
                        "chat_completion", prompt_tokens,
                        latency_ms, ttft_ms, success=True
                    )
                    resp.success()
                except Exception as e:
                    resp.failure(f"Parse error: {e}")
                    record_custom("chat_completion", 0, latency_ms, 0, success=False)
            else:
                resp.failure(f"HTTP {resp.status_code}: {resp.text[:200]}")
                record_custom("chat_completion", 0, latency_ms, 0, success=False)

    @task(1)
    def health_check(self):
        """Lightweight health probe — lower weight so it doesn't skew latency stats."""
        with self.client.get("/health", catch_response=True, name="GET /health") as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Health check failed: {resp.status_code}")


# ─── CSV DUMP ON TEST STOP ────────────────────────────────────────────────────

@events.quitting.add_listener
def dump_custom_csv(environment, **kwargs):
    if not _custom_rows:
        return

    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, "vllm_custom_metrics.csv")
    fields = ["timestamp", "request_name", "prompt_tokens",
              "latency_ms", "ttft_ms", "success"]

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(_custom_rows)

    print(f"\n✅  Custom metrics saved → {path}  ({len(_custom_rows)} rows)")

    # Also print a quick summary to stdout
    success = [r for r in _custom_rows if r["success"]]
    fail    = [r for r in _custom_rows if not r["success"]]
    if success:
        avg_lat  = sum(r["latency_ms"] for r in success) / len(success)
        avg_ttft = sum(r["ttft_ms"]    for r in success) / len(success)
        print(f"   Total requests : {len(_custom_rows)}")
        print(f"   Successful     : {len(success)}")
        print(f"   Failed         : {len(fail)}")
        print(f"   Avg latency    : {avg_lat:.0f} ms")
        print(f"   Avg TTFT       : {avg_ttft:.0f} ms")


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print(f"🚀  vLLM load test starting — results will be saved to ./{RESULTS_DIR}/")