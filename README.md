# End-to-End-Data-Pipeline
This project implements a production-style data pipeline using Apache Spark and a lakehouse architecture.

## Pipeline Architecture

Raw Data
   ↓
Pre Cleaner
   ↓
Bronze Layer (Raw → Parquet)
   ↓
Semantic Transformation (Canonical schema)
   ↓
Standardized Layer
   ↓
Data Quality Engine
   ↓
Silver Layer
   ├── valid
   ├── quarantine
   └── critical
   ↓
Gold Layer (Business Metrics)

## Tech Stack

- Apache Spark (PySpark)
- Parquet
- YAML configuration
- Lakehouse architecture
- Data Quality Engine

## Features

• Dataset-independent pipeline  
• Schema standardization  
• Config-driven data quality rules  
• Classification into VALID / QUARANTINE / CRITICAL  
• Automated Spark pipeline execution 
PIPELINE STRUCTURE
             +--------------+
             | Raw Dataset  |
             +--------------+
                     |
                     v
             +--------------+
             | Pre Cleaner  |
             +--------------+
                     |
                     v
             +--------------+
             | Bronze Layer |
             +--------------+
                     |
                     v
        +---------------------------+
        | Semantic Transformation   |
        +---------------------------+
                     |
                     v
           +--------------------+
           | Standardized Layer |
           +--------------------+
                     |
                     v
           +--------------------+
           | Data Quality Engine|
           +--------------------+
                     |
         +-----------+-----------+
         |                       |
         v                       v
   Valid Records          Quarantine Records
         |
         v
     Gold Analytics
