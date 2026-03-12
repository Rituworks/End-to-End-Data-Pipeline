from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    lit, current_timestamp
)

# -------------------------
# Spark Session
# -------------------------
spark = (
    SparkSession.builder
    .appName("DQReviewBuilder")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

print("✅ Spark started for DQ Review Builder")

# -------------------------
# Paths
# -------------------------
QUARANTINE_PATH = "lake/silver/quarantine"
DQ_PENDING_PATH = "lake/dq_review/pending"

# -------------------------
# Read Quarantine Data
# -------------------------
df = spark.read.parquet(QUARANTINE_PATH)
print("📥 Quarantine data loaded")

# -------------------------
# Add Review Metadata
# -------------------------
review_df = (
    df
    .withColumn("review_status", lit("PENDING"))
    .withColumn("reviewed_by", lit(None).cast("string"))
    .withColumn("review_comment", lit(None).cast("string"))
    .withColumn("review_created_at", current_timestamp())
)

# -------------------------
# Write to DQ Review Pending
# -------------------------
review_df.write.mode("append").parquet(DQ_PENDING_PATH)

print("✅ DQ Review Pending layer written")
print("🏁 DQ Review Builder complete")
