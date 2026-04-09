# Benchmark Result Interpretations

I ran my first benchmark on RTX 4090 and model was ```NousResearch/Hermes-3-Llama-3.1-8B```. 
Below stats are not that good and let's learn to interpret them so we can optimise them.

## Summary
```
- **Successful requests:** 1000
- **Failed requests:** 0
- **Benchmark duration (s):** 194.26
- **Total input tokens:** 1,023,000
- **Total generated tokens:** 128,000
- **Request throughput (req/s):** 5.15
```

Interpretation:

- The system completes about 5 requests per second on average.
- This does **not** mean each incoming request is served immediately.
- This is an average metric: almost all 1,000 requests took more than 1 second to complete, but batching affects the aggregate average.

---

## Throughput Metrics

```
- **Output token throughput (tok/s):** 658.92
- **Peak output token throughput (tok/s):** 1547.00
- **Total token throughput (tok/s):** 5925.09
```

Interpretation:

- Each request has a different size.
- At some points, output throughput peaked at 1547 tok/s.
- The average output token throughput is generally the more reliable metric.
- This is sum of input and output token throughput.

## Time to First Token (TTFT)

```
- **Mean TTFT (ms):** 96297.21
- **Median TTFT (ms):** 96648.12
- **P99 TTFT (ms):** 187987.54
```

Interpretation:

- On average, one request took about 96 seconds before users saw the first token.
- 50% of users waited between 0 to 96 seconds; the remaining 50% waited longer than 96 seconds.
- 99% of users waited between 0 and 187 seconds; the remaining 1% waited longer than 187 seconds.

---

## Time per Output Token (TPOT, excluding first token)

```
- **Mean TPOT (ms):** 50.64 [Around 20 tokens per second, humans read 5 to 10 tokens per second]
- **Median TPOT (ms):** 49.83
- **P99 TPOT (ms):** 72.50
```

This metric is useful when tokens are **not streamed**, meaning users do not see tokens immediately.  
Focus on this metric for model efficiency.

---

## Inter-Token Latency (ITL)

```
- **Mean ITL (ms):** 50.64
- **Median ITL (ms):** 24.94
- **P99 ITL (ms):** 213.89
```

- ITL starts from the **second token** (the first token has no predecessor).
- This is useful when tokens are streamed and users see output in real time (for example, in chatbots).
- Here, 99% of users waited between 0 and 0.22 seconds between two tokens.
- While the average is about 50 ms, a P99 of 213 ms indicates occasional stuttering.
- Not good for streaming applications; otherwise acceptable.
- This metric reflects user-perceived responsiveness.

