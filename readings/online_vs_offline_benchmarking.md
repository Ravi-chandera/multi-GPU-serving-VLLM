# Online vs Offline Benchmarking in vLLM.

Online benchmarking in vLLM measures the performance of a running API server by sending requests over HTTP, simulating real-world serving scenarios. We use online benchmarking (e.g., vllm bench serve) when we want to evaluate end-to-end latency, throughput, and concurrency as experienced by API clients, including server-side overheads. 

Here is how sample benchmark output looks like
```
============ Serving Benchmark Result ============
Successful requests:                     10
Benchmark duration (s):                  5.78
Total input tokens:                      1369
Total generated tokens:                  2212
Request throughput (req/s):              1.73
Output token throughput (tok/s):         382.89
Total token throughput (tok/s):          619.85
---------------Time to First Token----------------
Mean TTFT (ms):                          71.54
Median TTFT (ms):                        73.88
P99 TTFT (ms):                           79.49
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          7.91
Median TPOT (ms):                        7.96
P99 TPOT (ms):                           8.03
---------------Inter-token Latency----------------
Mean ITL (ms):                           7.74
Median ITL (ms):                         7.70
P99 ITL (ms):                            8.39
==================================================
```

Offline benchmarking, on the other hand, directly invokes the model in-process via the Python API, bypassing the HTTP server. We use offline benchmarking to measure raw model inference speed, ideal for hardware or model-level optimization without server overhead. This is mostly used when we are writing custom GPU kernerls for model level optimizations. 

Here is how sample benchmark output looks like
```
Throughput: 7.15 requests/s
4656.00 total tokens/s
1072.15 output tokens/s
Total num prompt tokens:  5014
Total num output tokens:  1500
```

Since I am deploying LLM for real world user experience, I will do online benchmarking. 
May be some day I will get chance to write kernels and will do offline benchmarking.