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
## Architecture Diagram


                 ┌──────────────────────────────┐
                 │    Python Simulator          │
                 │ (simulator_pushgateway.py)   │
                 └────────────┬─────────────────┘
                              │
                              ▼
                 ┌──────────────────────────────┐
                 │      Prometheus PushGateway  │
                 └────────────┬─────────────────┘
                              │
                              ▼
                 ┌──────────────────────────────┐
                 │          Prometheus          │
                 │ (Scrapes metrics & triggers  │
                 │  alerts based on rules)      │
                 └──────┬──────────┬────────────┘
                        │          │
                        │          ▼
                        │  ┌────────────────────┐
                        │  │   Grafana          │
                        │  │ (Dashboards only)  │
                        │  └────────────────────┘
                        ▼
        ┌────────────────────────────────────┐
        │         Alertmanager               │
        │ (Receives alerts from Prometheus  │
        │  and routes to webhook/email/SMS) │
        └────────────────────┬──────────────┘
                             ▼
                ┌────────────────────────────┐
                │   Flask Webhook Server     │
                │ (sendgrid_alert_webhook.py)│
                └────────────┬───────────────┘
                             ▼
                 Sends Email via SendGrid API


## Part 1: Monitoring Design

This monitoring setup is built to provide comprehensive observability into the health and performance of a server infrastructure. It is containerized using Docker Compose, and leverages Prometheus, Grafana, and custom Python scripts to simulate and collect metrics.

### Metrics Monitored
The following system-level metrics are continuously tracked and are simulated by metrics_simulator python script:

- **CPU Usage (%)** – Measures processing load  
- **Memory Usage (%)** – Indicates system memory consumption  
- **Disk Usage (%)** – Observes available vs. used disk space on root mount (`/`)  
- **Network Traffic (Inbound)** – Monitors bytes received per second  
- **Load Average (1-minute)** – Tracks system load over the last 1 minute  
- **Node Status (Up/Down)** – Verifies if node-exporter is active and reachable

---

### Tools / Scripts Used for Metric Collection

| Tool / Script              | Purpose                                                                 |
|---------------------------|-------------------------------------------------------------------------|
| `metrics_simulator.py`    | Simulates CPU, memory, disk, load, and network metrics for testing      |
| `pushgateway`             | Stores metrics pushed from short-lived scripts before Prometheus pulls |


**Bonus:** All components (Prometheus, Grafana, Node Exporter, PushGateway, Alertmanager) are defined in the `docker-compose.yml` file and can be launched together via `run.sh`.

---

### Backend Storage Solution

- **Prometheus** is used as the core time-series database and metrics collector.  
- It scrapes data from `node-exporter` and `Pushgateway`.  
- All metrics are stored, visualized in Grafana, and evaluated for alerting rules using `prometheus.yml` and `alert.rules.yml`.

## Part 2: Alerting

This section outlines the alerting strategy implemented using **Prometheus Alertmanager**, a **Python webhook server**, and **SendGrid email integration**.

### Alerting Strategy

- Alerts are triggered based on custom thresholds for each metric.
- Prometheus continuously evaluates conditions using **PromQL**.
- Alerts are grouped and routed to a **webhook receiver** (running on Flask) which then sends email alerts using the **SendGrid API**.

---

### Alert Rules Configuration

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

### Alert Delivery: Email via SendGrid

- **Webhook URL:** `http://localhost:5001/` (Flask server endpoint)
- **SendGrid API** is used to send email notifications for active alerts.
- Alerts include detailed annotations (`summary`, `description`) parsed by the webhook script and sent via email.

---

### Grafana Color Thresholds

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

## How Does Your Design Scale with Increased Servers or Monitoring Requirements?

### Answer:

To support scalability:

- I will **containerize my application** along with all key monitoring components — `Prometheus`, `Grafana`, `PushGateway`, `Node Exporter`, and `AlertManager`.
- I will **deploy the entire stack on Kubernetes**, where:
  - Each service and the application will run inside individual **Pods**.
  - **Prometheus** will scrape metrics from all pods or nodes in the cluster.
  - Kubernetes’ **Horizontal Pod Autoscaler (HPA)** will scale the application and services automatically based on CPU usage or custom metrics.
  - **Helm Charts** or **Kubernetes Deployments** will allow easy scaling, reproducibility, and management.

### Benefits of This Design:

- **Self-healing**: Failed containers are restarted automatically.
- **Scalable**: Easily add new monitoring targets or replicas.
- **Flexible**: Add more nodes or services without modifying the monitoring setup.
- **Extensible**: Supports additional tools like Loki, Tempo, or service meshes.

This Kubernetes-based architecture ensures that both the application and monitoring stack scale seamlessly with infrastructure growth.

____

---

## Run Instructions

Follow the steps below to set up and run the monitoring system locally:

### 1. Clone the Repository

```bash
git clone https://github.com/likhithakotla/devops_monitoring_with_twilio_and_grafana.git
cd devops_monitoring_with_twilio_and_grafana
```

### 2. Add the `.env` File

- Add the .env file before running:

- Fill in the required environment variables in `.env`:

```env
SENDGRID_API_KEY=your_actual_sendgrid_api_key
FROM_EMAIL=your_verified_sender@example.com
TO_EMAIL=recipient@example.com
```

### 3. Run the `run.sh` Script

- Make the script executable (if not already):

```bash
chmod +x run.sh
```
- Execute it to start all Docker containers:

```bash
./run.sh
```

This will spin up the following services using Docker:
- Prometheus
- Grafana
- AlertManager
- Node Exporter
- PushGateway

![Container_Running_and_installation_of_all_the_dependencies](screenshots/container start.png)

### 4. Run Python Scripts

- Open **two terminal windows**:
  - **Terminal 1**: Start the metric simulator

```bash
python3 metrics_simulator.py
```
![Pushed_Matrics](screenshots/Pushed Simulator matrics.png)

  - **Terminal 2**: Start the SendGrid webhook server

```bash
python3 twilio_alert_webhook.py
```
![Alert_Message](screenshots/alert message.png)

### 5. (Optional) Run Webhook in Production Mode

If deploying in production, use Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 twilio_alert_webhook:app
```

### 6. Access Prometheus

- URL: [http://localhost:9090](http://localhost:9090)
- Navigate to the **Alerts** tab to view active alerts.

![Prometheus alerts](screenshots/Prometheus.png)

### 7. Access Grafana Dashboards

- URL: [http://localhost:3000](http://localhost:3000)
- Login:
  - Username: `admin`
  - Password: `admin`
- View and explore:
  - CPU Usage
  - Memory Usage
  - Disk Space
  - Node Status
  - Load Average
  - Network Traffic

![Dashboards](screenshots/all dashboards.png)
![Dashboards](screenshots/all dashboards 2.png)
![Dashboards](screenshots/all dashboards 3.png)
![Dashboard](screenshots/CPU usage dashboard.png)

### 8. Alerts to Email
- If threshold is reached alerts are generated to with the email subject and message as shown. 

![Emails](screenshots/Emails screenshot.png)

### 9. Stop running containers
- Run docker-compose down
---

