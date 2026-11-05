from pyspark.sql import SparkSession
from pyspark.sql.functions import count, col

# Create Spark session
spark = SparkSession.builder \
    .appName("SmartCity311") \
    .master("local[*]") \
    .getOrCreate()

print("Spark Started Successfully!")

# Load cleaned dataset
df = spark.read.csv(
    "data/processed/311_cleaned.csv",
    header=True,
    inferSchema=True
)

# Total complaints
print("TOTAL COMPLAINTS:", df.count())

# Top complaint types
print("TOP 10 COMPLAINT TYPES")

df.groupBy("complaint_type") \
    .agg(count("*").alias("total")) \
    .orderBy(col("total").desc()) \
    .show(10, truncate=False)

# Borough analysis
print("BOROUGH-WISE COMPLAINTS")

df.groupBy("borough") \
    .count() \
    .orderBy(col("count").desc()) \
    .show()

# Save output
import os
os.makedirs("data/processed", exist_ok=True)
result = df.groupBy("complaint_type").count().toPandas()

os.makedirs("data/processed", exist_ok=True)

result.to_csv(
    "data/processed/pyspark_output.csv",
    index=False
)