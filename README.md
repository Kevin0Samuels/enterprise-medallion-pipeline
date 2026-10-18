# Enterprise-Grade Medallion Data Pipeline (DATA-1)

An automated, configuration-driven data engineering platform implementing a Medallion Architecture (Bronze → Silver → Gold) for multi-tenant e-commerce analytics. It is built on local object storage and a high-performance columnar data warehouse for scalable, domain-oriented data processing.

## Architecture & Tech Stack

- Orchestration & Infrastructure: Docker Compose, Apache Airflow
- Object Storage: MinIO (S3-compatible storage for raw ingestion)
- Data Warehouse & Query Engine: ClickHouse (columnar storage, external S3 engine, and `ReplacingMergeTree` deduplication)
- Processing Language: Python 3.11 (`pandas`, `pyarrow`, `clickhouse-connect`)

## Project Structure

```text
.
├── docker-compose.yml              # Orchestrates MinIO, ClickHouse, and Airflow
├── generate_data.py                # Synthetic e-commerce data generator (10 tables)
├── upload_to_minio.py              # Pushes raw ORC files into MinIO storage buckets
├── create_bronze_tables.py         # Provisions ClickHouse external S3 tables with partitions
├── create_silver_tables.py         # Cleans, types, and deduplicates data via ReplacingMergeTree
├── create_gold_tables.py           # Multi-tenant business aggregation tables
├── schema_helper.py                # Standalone CLI for auto-generating Bronze YAML configs
├── test_collision.py               # Automated test proving strict multi-tenant key isolation
├── data_output/                   # Local staging ground for generated ORC files
└── README.md
```

## Quickstart Guide

### 1. Spin up infrastructure

Start local MinIO, ClickHouse, and Airflow containers:

```bash
docker compose up -d
```

### 2. Generate and upload synthetic data

Generate mock e-commerce records across 10 tables and push them into MinIO:

```bash
python3 generate_data.py
python3 upload_to_minio.py
```

### 3. Build the data pipeline layers

#### Bronze layer (raw ingestion)

```bash
python3 create_bronze_tables.py
```

#### Silver layer (cleaning and deduplication)

```bash
python3 create_silver_tables.py
```

#### Gold layer (multi-tenant aggregations)

```bash
python3 create_gold_tables.py
```

## Key Architectural Highlights

### Multi-Tenant Isolation & Collision Proof

The platform enforces strict data boundaries between independent organizations through `organisation_id`. A dedicated test suite (`test_collision.py`) verifies that identical business keys such as `usr_999` remain distinct and isolated across organizations, preventing cross-tenant data leakage.

### Columnar Performance & Zero-Copy Ingestion

The pipeline uses Apache ORC file formats and ClickHouse's S3 table engine to query raw data directly from object storage before transforming it into high-performance primary-key structures.

### Schema Auto-Configuration CLI

A standalone helper tool, `schema_helper.py`, inspects raw ORC schemas via PyArrow and auto-generates structured Bronze YAML configuration drafts to reduce manual setup and schema drift.