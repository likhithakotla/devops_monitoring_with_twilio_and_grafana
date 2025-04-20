import time
import random
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()

cpu_usage = Gauge('custom_cpu_usage', 'Simulated CPU Usage (%)', registry=registry)
memory_usage = Gauge('custom_memory_usage', 'Simulated Memory Usage (%)', registry=registry)
disk_avail = Gauge('node_filesystem_avail_bytes', 'Available disk space in bytes', ['mountpoint'], registry=registry)
disk_total = Gauge('node_filesystem_size_bytes', 'Total disk size in bytes', ['mountpoint'], registry=registry)
node_up = Gauge('up', 'Simulate node status (1 = up, 0 = down)', ['job'], registry=registry)
load_avg = Gauge('node_load1', '1-minute load average', registry=registry)
net_rx = Gauge('node_network_receive_bytes_total', 'Total network bytes received', ['device'], registry=registry)
# swap_total = Gauge('node_memory_SwapTotal_bytes', 'Total swap space', registry=registry)
# swap_free = Gauge('node_memory_SwapFree_bytes', 'Free swap space', registry=registry)
# fd_allocated = Gauge('node_filefd_allocated', 'Allocated file descriptors', registry=registry)
# fd_max = Gauge('node_filefd_maximum', 'Max file descriptors', registry=registry)

while True:
    cpu = random.uniform(40, 95)
    mem = random.uniform(50, 90)
    disk_size = 1e9
    disk_free = random.uniform(1e7, 1.5e8)
    load = random.uniform(0.5, 3.5)
    net_bytes = random.uniform(1e6, 2e8)
    # swap_t = 1e8
    # swap_f = random.uniform(1e6, 7e7)
    # fd_used = random.uniform(80000, 95000)
    # fd_limit = 100000

    cpu_usage.set(cpu)
    memory_usage.set(mem)
    disk_avail.labels(mountpoint='/').set(disk_free)
    disk_total.labels(mountpoint='/').set(disk_size)
    node_up.labels(job='node-exporter').set(1)
    load_avg.set(load)
    net_rx.labels(device='eth0').inc(net_bytes)
    # swap_total.set(swap_t)
    # swap_free.set(swap_f)
    # fd_allocated.set(fd_used)
    # fd_max.set(fd_limit)

    push_to_gateway('localhost:9091', job='custom_simulator', registry=registry)
    print("=== Metrics Pushed ===")
    print(f"🧠 CPU Usage: {cpu:.2f}%")
    print(f"💾 Memory Usage: {mem:.2f}%")
    print(f"📀 Disk Available: {disk_free / 1e6:.2f} MB")
    print(f"📊 Load Avg (1m): {load:.2f}")
    print(f"🌐 Network Rx: {net_bytes / 1e6:.2f} MB")
    # print(f"💽 Swap Used: {(swap_t - swap_f) / 1e6:.2f} MB / {swap_t / 1e6:.2f} MB")
    # print(f"📂 File Descriptors: {fd_used:.0f} / {fd_limit}")
    print("=======================\n")
    time.sleep(10)
