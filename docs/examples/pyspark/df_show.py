import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, LongType, StringType, IntegerType, DateType, TimestampType, FloatType
from pyspark.sql.functions import col, cast, date_trunc, sum, dayofweek, hour, dayofmonth, lit

# запуск spark
spark = SparkSession.builder.appName('show').getOrCreate()

# формирование dataframe
values= [
        (4,4.0,'4'),
        (5,5.0,'5'),
        (6,6.0,'6')
    ]

schemaData = StructType([ \
    StructField("c1",IntegerType(),True), 
    StructField("c2",FloatType(),True), 
    StructField("c3",StringType(),True)
  ])

df = spark.createDataFrame(values,schema=schemaData)
df.show(3,False)

spark.stop()
