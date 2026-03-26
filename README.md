# End-to-End Data Pipeline (Apache Spark)

## 📌 Overview

This project implements a scalable end-to-end data pipeline using Apache Spark and a lakehouse architecture. The pipeline processes raw transactional data, standardizes it into a canonical schema, applies data quality checks, and generates business-ready analytics.

---

## 🚀 Problem Statement

Raw datasets are often inconsistent, unstructured, and unreliable for analytics.
This pipeline transforms raw data into clean, validated, and structured data that can be used for business insights and decision-making.

---

## 🏗️ Architecture


Raw Data
   ↓
Pre Cleaner
   ↓
Bronze Layer (Raw → Parquet)
   ↓
Semantic Transformation (Canonical Schema)
   ↓
Standardized Layer
   ↓
Data Quality Engine
   ↓
Silver Layer
   ├── Valid Data
   ├── Quarantine Data
   └── Critical Data
   ↓
Gold Layer (Business Metrics)


---

## ⚙️ Tech Stack

* Apache Spark (PySpark)
* Python
* Parquet (Columnar Storage)
* YAML (Config-driven rules)
* Git & GitHub
* Linux (WSL)

---

## 🔍 Key Features

* End-to-end data pipeline using lakehouse architecture
* Schema standardization using canonical data model
* Data Quality Engine with severity classification:

  * VALID → clean data
  * QUARANTINE → suspicious data
  * CRITICAL → invalid/broken data
* Fraud-aware processing (fraud records preserved)
* Scalable batch processing using Apache Spark
* Config-driven pipeline design

---

## 📊 Sample Output

### Data Quality Metrics


VALID        → 6,362,620 records
QUARANTINE   → 8,000 records
CRITICAL     → 2,000 records


### Business Metrics


Date        Total Transactions   Total Amount   Avg Transaction
2026-03-12  120000               3,400,000      28.3


---

## ▶️ How to Run

### Step 1: Run Individual Jobs


spark-submit spark_jobs/pre_cleaner.py
spark-submit spark_jobs/semantic_transform.py
spark-submit spark_jobs/silver_cleaner_v2.py
spark-submit spark_jobs/gold_daily_metrics.py


### Step 2: Run Full Pipeline


python run_pipeline.py


---

## 📂 Project Structure


spark_jobs/
    pre_cleaner.py
    semantic_transform.py
    silver_cleaner_v2.py
    gold_daily_metrics.py

configs/
    canonical_schema.json
    dq_rules.yaml

run_pipeline.py
README.md




## 💡 Key Learnings

* Designing scalable data pipelines
* Working with distributed data processing using Spark
* Implementing data quality frameworks
* Schema standardization across datasets
* Building production-style data workflows

---

## 🎯 Future Improvements

* Data Quality Dashboard (metrics monitoring)
* Pipeline orchestration with scheduling (Airflow)
* Real-time streaming pipeline integration
* Advanced fraud detection logic

---


Ritu
GitHub: https://github.com/Rituworks
