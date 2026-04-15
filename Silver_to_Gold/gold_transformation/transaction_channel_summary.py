count = spark.sql("""
  SELECT COUNT(*) AS cnt
  FROM banking.gold.transaction_channel_summary
  """).collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
