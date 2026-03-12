import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date

# -------------------------
# Paths
# -------------------------

INPUT_DIR = "uploads_input"
BRONZE_PATH = "lake/bronze"
PROCESSED_PATH = "lake/metadata/processed_files"

# -------------------------
# Spark Session
# -------------------------

spark = (
    SparkSession.builder
    .appName("PreCleanerEngine")
    .getOrCreate()
)

print("✅ Spark session started")

# -------------------------
# Load processed files
# -------------------------

try:
    processed_df = spark.read.parquet(PROCESSED_PATH)
    processed_files = [row.file_name for row in processed_df.collect()]
    print(f"📂 Already processed files: {processed_files}")
except:
    processed_files = []
    print("📂 No processed files metadata found")

# -------------------------
# Detect new files
# -------------------------

files = [
    f for f in os.listdir(INPUT_DIR)
    if f.endswith(".csv") and f not in processed_files
]

if not files:
    print("⚠️ No new files found to process")
    exit(0)

# -------------------------
# Process each file
# -------------------------

for file in files:

    print(f"📥 Processing file: {file}")

    file_path = f"{INPUT_DIR}/{file}"

    df = spark.read.csv(
        file_path,
        header=True,
        inferSchema=True
    )

    df = df.withColumn("ingestion_date", current_date())

    # Write to Bronze
    (
        df.write
        .mode("append")
        .parquet(BRONZE_PATH)
    )

    print(f"✅ Written to Bronze: {file}")

    # Log processed file
    log_df = spark.createDataFrame([(file,)], ["file_name"])

    (
        log_df.write
        .mode("append")
        .parquet(PROCESSED_PATH)
    )

    print(f"📝 Logged processed file: {file}")

print("🏁 Bronze ingestion completed successfully")