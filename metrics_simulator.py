import time
import random
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()

cpu_usage = Gauge('custom_cpu_usage', 'Simulated CPU Usage (%)', registry=registry)
memory_usage = Gauge('custom_memory_usage', 'Simulated Memory Usage (%)', registry=registry)
disk_avail = Gauge('node_filesystem_avail_bytes', 'Available disk space in bytes', ['mountpoint'], registry=registry)
disk_total = Gauge('node_filesystem_size_bytes', 'Total disk size in bytes', ['mountpoint'], registry=registry)
# node_up = Gauge('up', 'Simulate node status (1 = up, 0 = down)', ['job'], registry=registry)
load_avg = Gauge('node_load1', '1-minute load average', registry=registry)
net_rx = Gauge('node_network_receive_bytes_total', 'Total network bytes received', ['device'], registry=registry)


while True:
    cpu = random.uniform(40, 95)
    mem = random.uniform(50, 90)
    disk_size = 1e9
    disk_free = random.uniform(1e7, 1.5e8)
    load = random.uniform(0.5, 3.5)
    net_bytes = random.uniform(1e6, 2e8)


    cpu_usage.set(cpu)
    memory_usage.set(mem)
    disk_avail.labels(mountpoint='/').set(disk_free)
    disk_total.labels(mountpoint='/').set(disk_size)
    # node_up.labels(job='node-exporter').set(1)
    load_avg.set(load)
    net_rx.labels(device='eth0').inc(net_bytes)


    push_to_gateway('localhost:9091', job='custom_simulator', registry=registry)
    print("=== Metrics Pushed ===")
    print(f"🧠 CPU Usage: {cpu:.2f}%")
    print(f"💾 Memory Usage: {mem:.2f}%")
    print(f"📀 Disk Available: {disk_free / 1e6:.2f} MB")
    print(f"📊 Load Avg (1m): {load:.2f}")
    print(f"🌐 Network Rx: {net_bytes / 1e6:.2f} MB")

    print("=======================\n")
    time.sleep(10)
