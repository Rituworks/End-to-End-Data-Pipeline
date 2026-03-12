import subprocess
import time

print("🚀 Starting End-to-End Data Pipeline")

jobs = [
    "spark_jobs/pre_cleaner.py",
    "spark_jobs/semantic_transform.py",
    "spark_jobs/silver_cleaner_v2.py",
    "spark_jobs/gold_daily_metrics.py",
    "spark_jobs/gold_fraud_metrics.py",
    "spark_jobs/dq_review_builder.py"
]

for job in jobs:

    print(f"\n▶ Running job: {job}")

    start = time.time()

    result = subprocess.run(
        ["spark-submit", job],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print("❌ Job failed:", job)
        print(result.stderr)
        break

    end = time.time()

    print(f"✅ Completed {job} in {round(end-start,2)} seconds")

print("\n🏁 Pipeline execution finished")