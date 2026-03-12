import yaml
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, lit, current_timestamp

spark = (
    SparkSession.builder
    .appName("SilverDQEngine")
    .getOrCreate()
)

print("⚙️ Starting Data Quality Engine")

STANDARDIZED_PATH = "lake/standardized"

VALID_PATH = "lake/silver/valid"
QUARANTINE_PATH = "lake/silver/quarantine"
CRITICAL_PATH = "lake/silver/critical"

# ------------------------
# Load standardized data
# ------------------------

df = spark.read.parquet(STANDARDIZED_PATH)

# ------------------------
# Load DQ rules
# ------------------------

with open("configs/dq_rules.yaml", "r") as file:
    dq_rules = yaml.safe_load(file)

rules = dq_rules["rules"]

# Default status
df = df.withColumn("dq_status", lit("VALID"))
df = df.withColumn("dq_reason", lit(None))

# ------------------------
# Apply rules
# ------------------------

for rule in rules:

    condition = rule["condition"]
    severity = rule["severity"]
    reason = rule["reason"]

    df = df.withColumn(
        "dq_status",
        expr(f"""
        CASE
        WHEN {condition} THEN '{severity}'
        ELSE dq_status
        END
        """)
    )

    df = df.withColumn(
        "dq_reason",
        expr(f"""
        CASE
        WHEN {condition} THEN '{reason}'
        ELSE dq_reason
        END
        """)
    )

df = df.withColumn("dq_processed_at", current_timestamp())

# ------------------------
# Split data
# ------------------------

valid_df = df.filter("dq_status = 'VALID'")
quarantine_df = df.filter("dq_status = 'QUARANTINE'")
critical_df = df.filter("dq_status = 'CRITICAL'")

# ------------------------
# Write results
# ------------------------

valid_df.write.mode("overwrite").parquet(VALID_PATH)

quarantine_df.write.mode("overwrite").parquet(QUARANTINE_PATH)

critical_df.write.mode("overwrite").parquet(CRITICAL_PATH)

print("✅ Data Quality classification completed")