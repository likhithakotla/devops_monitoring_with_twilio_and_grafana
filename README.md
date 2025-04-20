# DevOps Monitoring & Alerting Assessment

## Architecture Summary

This project sets up a complete **Monitoring + Alerting** solution using Docker containers, Prometheus, Grafana, and SendGrid webhook-based alerting.
**Optional** : Node exporter is only used for real time metrics uncomment if needed. 

**Components in Containers:**
- **Node Exporter**: Provides host metrics (Uncomment it if you need real host matrics but in this Assessment we are Simulating fake metrics from metrics_simulator code)
- **Pushgateway**: Accepts metrics from short-lived scripts
- **Prometheus**: Stores and evaluates metrics
- **Alertmanager**: Sends notifications based on alert rules
- **Grafana**: Visualizes metrics through dashboards

**Custom Scripts:**
- **metrics_simulator.py**: Simulates metrics (CPU, memory, disk, network)
- **twilio_alert_webhook.py**: Flask server for receiving webhook alerts
- **sendgrid_config.py**: SendGrid setup for API email delivery
- **run.sh**: Orchestrates startup of all services and installs all dependencies.

**Key Files:**
| File | Purpose |
|------|---------|
| `docker-compose.yml` | Spins up Prometheus, Grafana, Pushgateway, Node Exporter(optional), Alertmanager |
| `prometheus.yml` | Defines scrape jobs for Prometheus |
| `alert.rules.yml` | Prometheus alert rules configuration |
| `system_alert_dashboard.json` | Grafana dashboard for visualizing metrics |
| `alertmanager.yml` | Routes alerts to SendGrid webhook |
| `metrics_simulator.py` | Python script to simulate and push metrics |
| `twilio_alert_webhook.py` | Receives webhooks and logs/email alerts |
| `sendgrid_config.py` | SendGrid API key configuration |
| `run.sh` | Script to start containers and install dependencies |

---

## 📈 Part 1: Monitoring Design

This monitoring setup is built to provide comprehensive observability into the health and performance of a server infrastructure. It is containerized using Docker Compose, and leverages Prometheus, Grafana, and custom Python scripts to simulate and collect metrics.

### ✅ Metrics Monitored
The following system-level metrics are continuously tracked and are simulated by metrics_simulator python script:

- **CPU Usage (%)** – Measures processing load  
- **Memory Usage (%)** – Indicates system memory consumption  
- **Disk Usage (%)** – Observes available vs. used disk space on root mount (`/`)  
- **Network Traffic (Inbound)** – Monitors bytes received per second  
- **Load Average (1-minute)** – Tracks system load over the last 1 minute  
- **Node Status (Up/Down)** – Verifies if node-exporter is active and reachable

---

### 🛠️ Tools / Scripts Used for Metric Collection

| Tool / Script              | Purpose                                                                 |
|---------------------------|-------------------------------------------------------------------------|
| `metrics_simulator.py`    | Simulates CPU, memory, disk, load, and network metrics for testing      |
| `pushgateway`             | Stores metrics pushed from short-lived scripts before Prometheus pulls |


✅ **Bonus:** All components (Prometheus, Grafana, Node Exporter, PushGateway, Alertmanager) are defined in the `docker-compose.yml` file and can be launched together via `run.sh`.

---

### 🗃️ Backend Storage Solution

- **Prometheus** is used as the core time-series database and metrics collector.  
- It scrapes data from `node-exporter` and `Pushgateway`.  
- All metrics are stored, visualized in Grafana, and evaluated for alerting rules using `prometheus.yml` and `alert.rules.yml`.

## 🚨 Part 2: Alerting

This section outlines the alerting strategy implemented using **Prometheus Alertmanager**, a **Python webhook server**, and **SendGrid email integration**.

### 🔔 Alerting Strategy

- Alerts are triggered based on custom thresholds for each metric.
- Prometheus continuously evaluates conditions using **PromQL**.
- Alerts are grouped and routed to a **webhook receiver** (running on Flask) which then sends email alerts using the **SendGrid API**.

---

### 📑 Alert Rules Configuration

Defined in `alert.rules.yml` and mounted into Prometheus:

| **Alert Name**        | **Condition (PromQL Expression)**                                                                 | **For Duration** | **Severity** | **Summary**                         |
|-----------------------|--------------------------------------------------------------------------------------------------|------------------|--------------|-------------------------------------|
| HighCPUUsage          | `custom_cpu_usage > 70`                                                                           | 2 minutes        | Critical     | High CPU usage detected             |
| HighMemoryUsage       | `custom_memory_usage > 50`                                                                        | 2 minutes        | Warning      | High Memory usage detected          |
| LowDiskSpace          | `(node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) < 0.1` | 5 minutes        | Warning      | Low disk space                      |
| NodeDown              | `up{job="node-exporter"} == 0`                                                                    | 1 minute         | Critical     | Node exporter is down               |
| HighLoadAverage       | `node_load1 > 2`                                                                                  | 2 minutes        | Warning      | High 1-minute load average          |
| HighNetworkTraffic    | `rate(node_network_receive_bytes_total[1m]) > 100000000`                                          | 1 minute         | Info         | High inbound network traffic        |

---

### 📬 Alert Delivery: Email via SendGrid

- **Webhook URL:** `http://localhost:5001/` (Flask server endpoint)
- **SendGrid API** is used to send email notifications for active alerts.
- Alerts include detailed annotations (`summary`, `description`) parsed by the webhook script and sent via email.

---

### 🎨 Grafana Color Thresholds

For better visualization, each panel is configured with color-coded thresholds in the dashboard JSON (`system_alert_dashboard.json`):

| **Metric**               | **Green** | **Orange** | **Red** |
|--------------------------|-----------|------------|---------|
| CPU Usage (%)            | `< 70`    | `70 - 90`  | `> 90`  |
| Memory Usage (%)         | `< 50`    | `50 - 90`  | `> 90`  |
| Disk Available (%)       | `> 30`    | `15 - 30`  | `< 15`  |
| Node Exporter Status     | `1` (Up)  | —          | `0` (Down) |
| Load Average (1 min)     | `< 1`     | `1 - 2`    | `> 2`   |
| Network Inbound (Bps)    | `< 50MB/s`| `50-100MB/s`| `> 100MB/s` |

These visual thresholds make it easy to monitor system health at a glance.

---




