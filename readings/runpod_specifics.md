# Runpod Specifics

I intentionally chose RunPod over AWS for this project to study inference behavior, including tensor parallelism, KV cache dynamics, and quantization tradeoffs. AWS introduces extra variables such as managed networking, driver abstraction, and a much higher cost, about ten times more, which would have limited the number of experiments and slowed iteration. With RunPod at $3 per hour instead of $32, I was able to run four times as many experiments for the same budget, enabling a much quicker cycle of trying, troubleshooting, learning, and starting over.

The parallelism configurations and benchmarking methodology I used work the same on both Runpod and AWS. While the raw performance numbers are specific to RunPod’s A100 hardware, my primary focus was on understanding system behavior: how different parallelism strategies, loads, and memory usage affect performance. These insights apply regardless of the provider. If I were to move to production on AWS, I would repeat the same benchmarking process on the target hardware to adjust the numbers, but the overall methodology would remain unchanged.

I do not recommend RunPod for production environments. Proper deployment requires features like VPC isolation, IAM, compliance certifications, SLAs, and close integration with the existing data pipeline—features that RunPod does not currently offer. For these requirements, platforms such as AWS, GCP, or Azure are more appropriate choices.

Here are Runpod specific details that I faced during this deployment.

## 1. Root and workspace errors in Runpod

When we connect to our pod terminal, we are connected as root user. 
The root directory (/) on RunPod is ephemeral and usually capped at 20GB. Even if you move to workspace and do all the insatlls, they directly goes to root. When you start installing vLLM in venv, the pod will crash or give you "No space left on device" errors.

Inside workspace run command ```df -h``` and you will see your mouted disk space. Here I have 40 GB of space.

```
root@b42f7aaf202f:/workspace# df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay          20G   16M   20G   1% /
tmpfs            64M     0   64M   0% /dev
/dev/nvme1n1     40G     0   40G   0% /workspace  -------> This one is our space.
shm              47G     0   47G   0% /dev/shm
/dev/nvme0n1p2  1.8T   20G  1.7T   2% /usr/bin/nvidia-smi  ----> Since runpod is shared cluster, we see this but not usable.
tmpfs           252G     0  252G   0% /sys/fs/cgroup
tmpfs           252G   12K  252G   1% /proc/driver/nvidia
tmpfs           252G  4.0K  252G   1% /etc/nvidia/nvidia-application-profiles-rc.d
tmpfs            51G   36M   51G   1% /run/nvidia-persistenced/socket
tmpfs           252G     0  252G   0% /proc/asound
tmpfs           252G     0  252G   0% /proc/acpi
tmpfs           252G     0  252G   0% /proc/scsi
tmpfs           252G     0  252G   0% /sys/firmware
tmpfs           252G     0  252G   0% /sys/devices/virtual/powercap
```

## 2. Volumne disk vs Network volumne

In RunPod, the choice between Volume Disk and Network Volume usually comes down to whether you prioritize speed or data portability.

### 2.1 Volume Disk (Local Persistent Storage)
The Volume Disk is high-performance storage that is physically attached to the machine your GPU is running on.
- **Performance:** Fastest. Since it is local NVMe storage, it offers the lowest latency and highest throughput. It is ideal for intensive tasks like training models where IOPS (Input/Output Operations Per Second) are a bottleneck.
- **Persistence:** It survives a Pod Stop or Restart. However, if you Terminate (Delete) the Pod, the Volume Disk and all data on it are permanently deleted.
- **Pricing:**  
    - Running: ~$0.10 / GB / month. 
    - Stopped: ~$0.20 / GB / month. (Note: It is more expensive when the Pod is idle to encourage users to clean up unused local resources).
    - Best For: Active development, training runs, and temporary workspaces where speed is the primary concern and you don't mind the data being tied to that specific Pod.

### 2.2 Network Volume
A Network Volume is a standalone storage entity that exists independently of any specific Pod.
- **Performance:** Variable/Slower. Because data travels over the internal network, it is slower than a local disk. Expect speeds around 200–400 MB/s, though "High-Performance" tiers are faster.
- **Persistence:** Permanent. It exists until you manually delete it from the "Storage" tab. You can delete a Pod and later attach the same Network Volume to a completely new Pod to pick up where you left off.Portability: You can mount the same Network Volume to multiple Pods simultaneously (within the same data center). This is great for sharing a large dataset (1TB+) across a cluster of GPUs.
- **Pricing:**  
    - Standard: ~$0.07 / GB / month (cheaper than local volume disks).
    - High-Performance: ~$0.14 / GB / month.
    - Best For: Large datasets, model weight libraries, and "Serverless" workflows where you want to keep your data alive without paying for an idle GPU Pod.

In learning phase, I would just use pod for 1 hour and then do not use it so I am choosing volumne disk, it is cheaper for me.
