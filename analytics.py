import duckdb

# Connect to database
con = duckdb.connect("smartcity311.db")

# Load cleaned dataset
con.execute("""
CREATE OR REPLACE TABLE complaints AS
SELECT *
FROM read_csv_auto(
    'data/processed/311_cleaned.csv'
)
""")

print("\nTOTAL COMPLAINTS")

print(con.execute("""
SELECT COUNT(*) FROM complaints
""").fetchall())

print("\nTOP 10 COMPLAINT TYPES")

print(con.execute("""
SELECT complaint_type, COUNT(*) AS total
FROM complaints
GROUP BY complaint_type
ORDER BY total DESC
LIMIT 10
""").df())

print("\nBOROUGH-WISE COMPLAINTS")

print(con.execute("""
SELECT borough, COUNT(*) AS total
FROM complaints
GROUP BY borough
ORDER BY total DESC
""").df())

print("\nAGENCY-WISE COMPLAINTS")

print(con.execute("""
SELECT agency, COUNT(*) AS total
FROM complaints
GROUP BY agency
ORDER BY total DESC
""").df())

con.close()

print("\nSQL ANALYTICS COMPLETED!")