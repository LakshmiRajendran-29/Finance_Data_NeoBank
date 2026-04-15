count = spark.sql("""
SELECT COUNT(*) AS cnt
FROM banking.gold.daily_bank_kpi
""").collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
