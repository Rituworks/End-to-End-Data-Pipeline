from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SemanticTransactionTransform")
    .config("spark.hadoop.io.native.lib.available", "false")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem")
    .getOrCreate()
)

print("✅ Spark session started")



raw_df = spark.read.parquet("lake/bronze")


raw_df.show(5)
raw_df.printSchema()
from pyspark.sql.functions import col, lit, current_timestamp
def detect_transaction_id(df):
    for c in df.columns:
        if "txn" in c.lower() or "transaction" in c.lower() or "id" in c.lower():
            return c
    return None
def detect_user_id(df):
    for c in df.columns:
        if "user" in c.lower() or "customer" in c.lower() or "account" in c.lower() or "name" in c.lower():
            return c
    return None
def detect_amount(df):
    for c in df.columns:
        if "amount" in c.lower() or "amt" in c.lower() or "value" in c.lower():
            return c
    return None
def detect_event_time(df):
    for c in df.columns:
        if "time" in c.lower() or "date" in c.lower():
            return c
    return None
def detect_status(df):
    for c in df.columns:
        if "status" in c.lower() or "fraud" in c.lower():
            return c
    return None
txn_col = detect_transaction_id(raw_df)
user_col = detect_user_id(raw_df)
amt_col = detect_amount(raw_df)
time_col = detect_event_time(raw_df)
status_col = detect_status(raw_df)

curated_df = raw_df.select(
    col(txn_col).alias("transaction_id") if txn_col else lit(None).alias("transaction_id"),
    col(user_col).alias("user_id") if user_col else lit("UNKNOWN").alias("user_id"),
    col(amt_col).alias("amount") if amt_col else lit(0.0).alias("amount"),
    col(time_col).alias("event_time") if time_col else current_timestamp().alias("event_time"),
    col(status_col).alias("status") if status_col else lit("UNKNOWN").alias("status")
)

curated_df.show(5)
curated_df.write.mode("overwrite").parquet("curated_parquet/transactions")
print("✅ Curated data written to Parquet")
