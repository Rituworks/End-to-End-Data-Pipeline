from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, avg

SILVER_PATH = "lake/silver/valid"
GOLD_PATH = "lake/gold/daily_transactions"

spark = (
    SparkSession.builder
    .appName("GoldDailyTransactions")
    .getOrCreate()
)

print("🥇 Gold Layer Job Started")

# Read clean Silver data
df = spark.read.parquet(SILVER_PATH)

# Aggregate daily metrics
daily_metrics = (
    df.groupBy("ingestion_date")
      .agg(
          count("*").alias("total_transactions"),
          sum("amount").alias("total_amount"),
          avg("amount").alias("avg_transaction_amount")
      )
)

daily_metrics.show(5)

# Write Gold layer
(
    daily_metrics
    .write
    .mode("append")
    .parquet(GOLD_PATH)
)

print("✅ Gold daily transaction metrics written")