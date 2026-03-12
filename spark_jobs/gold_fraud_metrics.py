from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum, when, round
)

# Paths
SILVER_PATH = "/mnt/c/Users/HP/OneDrive/Desktop/upi data pipeline/lake/silver"
GOLD_PATH = "/mnt/c/Users/HP/OneDrive/Desktop/upi data pipeline/lake/gold/fraud_daily_metrics"

spark = (
    SparkSession.builder
    .appName("GoldFraudMetrics")
    .getOrCreate()
)

print("🥇 Gold Fraud Metrics job started")

# Read Silver layer
df = spark.read.parquet(SILVER_PATH)

# Aggregate fraud metrics
fraud_metrics = (
    df.groupBy("ingestion_date")
    .agg(
        count("*").alias("total_transactions"),
        sum(when(col("isFraud") == 1, 1).otherwise(0)).alias("fraud_transactions"),
        sum(when(col("isFraud") == 1, col("amount")).otherwise(0)).alias("fraud_amount")
    )
    .withColumn(
        "fraud_rate",
        round(col("fraud_transactions") / col("total_transactions"), 4)
    )
)

# Write Gold layer (overwrite is OK for metrics)
(
    fraud_metrics.write
    .mode("overwrite")
    .parquet(GOLD_PATH)
)

print("✅ Gold Fraud Metrics written successfully")

spark.stop()
