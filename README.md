# CPG Line Monitoring with Medallion Architecture

This project demonstrates a simulated end-to-end industrial data pipeline for a CPG (Consumer Packaged Goods) production line using the **Medallion Architecture (Bronze, Silver, Gold layers)** on **Databricks**, ingesting data from **Kafka**, and visualizing insights via **Power BI**.

---

## 📌 Use Case

Monitor real-time and historical performance of a packaging line using simulated sensor and batch data. Derive actionable insights like:

- Average temperature, humidity, and oil viscosity
- Conveyor speed trends
- Production counts by shift
- Batch-level performance summaries

---

## 🏗️ Architecture Overview

![Medallion Architecture](A_2D_digital_diagram_illustrates_a_medallion_archi.png)

---

## 💾 Data Sources

### 1. **Node-RED** (Simulated data publisher)
- Simulates sensor data and batch metadata
- Streams data to Kafka topics:
  - `cpg.line1.stream`
  - `cpg.line1.batch`

### 2. **Kafka**
- Locally containerized via Docker
- Topics:
  - **Stream**: real-time sensor metrics
  - **Batch**: planned vs produced quantities, shift metadata

---

## 🔁 Bronze Layer (Raw Delta Tables)

Created by consuming from Kafka topics into raw Delta Lake tables:
- `cpg_line1_stream`: sensor metrics
- `cpg_line1_batch`: batch plans

Transformation includes:
- Dropping and recreating existing tables
- Adding `ingest_time` column
- Archiving original Kafka payload in Delta Lake

---

## 🔄 Silver Layer (Cleaned / Enriched Tables)

### Stream Silver (`cpg_line1_stream_silver`)
- Filters out records with null temperature or timestamps
- Deduplicates and normalizes structure

### Batch Silver (`cpg_line1_batch_silver`)
- Retains key batch metadata: batchId, productCode, status, timestamps

---

## 🪙 Gold Layer (Aggregated Insights)

### 1. **Gold: Batch-Level Metrics**
- Joins stream & batch data by `batchId`
- Aggregates:
  - Average temperature, humidity, oil viscosity
  - Max belt speed
  - Record counts per batch

### 2. **Gold: Shift-Based Summary**
- Aggregates metrics by `shift` and `status`
- Calculates total quantity planned, produced, average conveyor speed, etc.

---

## 📊 Visualization (Optional)

- **Power BI / Databricks SQL** dashboards can be built on Gold tables.
- Useful charts:
  - Batch success/failure rates
  - Sensor anomalies by shift
  - Throughput trends by timestamp

---

## 🧪 How to Run

1. **Start local containers** (Kafka, Node-RED)
2. Simulate data flow
3. Execute notebooks in order:
   - `01-ingest-bronze`
   - `02-transform-silver`
   - `03-gold-aggregations`
4. Query the Gold tables for insights

---

## 🗂️ File Structure

```
├── README.md
├── docker-compose.yml
├── notebooks/
│   ├── 01-ingest-bronze.py
│   ├── 02-transform-silver.py
│   ├── 03-gold-aggregations.py
├── data/
│   ├── cpg.line1.stream.jsonl
│   ├── cpg.line1.batch.jsonl
├── images/
│   └── A_2D_digital_diagram_illustrates_a_medallion_archi.png
```

---

## ✅ Achievements

- Full pipeline design from edge simulation to Gold table generation
- Implemented Medallion Architecture on local + Databricks free tier
- Insightful aggregation logic prepared for visualization layer

---

## 📌 Next Steps

- Add ML model for predictive maintenance (e.g. anomaly detection)
- Schedule ETL jobs with workflows
- Publish live dashboard to Power BI
