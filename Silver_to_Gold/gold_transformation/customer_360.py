count = spark.sql("""
SELECT COUNT(*) AS cnt
FROM banking.gold.customer_360
""").collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
