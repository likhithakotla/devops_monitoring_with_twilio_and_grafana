#!/bin/bash

echo "Starting DevOps Monitoring System with SendGrid Email Alerts..."

# Step 1: Start Docker containers
echo "Starting Docker containers..."
docker-compose up -d
if [ $? -ne 0 ]; then
  echo "Failed to start Docker containers. Exiting."
  exit 1
fi

# Step 2: Install Python packages silently if not already installed
echo "Installing Python dependencies..."
pip show prometheus_client >/dev/null 2>&1 || pip install prometheus_client
pip show flask >/dev/null 2>&1 || pip install flask
pip show send grid >/dev/null 2>&1 || pip install sendgrid
pip show python-dotenv >/dev/null 2>&1 || pip install python-dotenv


echo "All services started!"
echo "Prometheus:    http://localhost:9090"
echo "Grafana:       http://localhost:3000  (admin/admin)"
echo "Alertmanager:  http://localhost:9093"
echo "Pushgateway:    http://localhost:9091"
echo "Node Exporter:  http://localhost:9100"
