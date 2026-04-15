count = spark.sql("""
SELECT COUNT(*) AS cnt
FROM banking.gold.branch_performance
""").collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
