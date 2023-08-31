import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, LongType, StringType, IntegerType, DateType, TimestampType, FloatType, BooleanType
from pyspark.sql.functions import col, cast, date_trunc, sum, dayofweek, hour, dayofmonth, lit, sequence

import random

# запуск spark
spark = SparkSession.builder.appName('parquet').getOrCreate()


schemaData = StructType([ \
    StructField("label",StringType(),True),
    StructField("feature1",IntegerType(),True), 
    StructField("feature2",FloatType(),True), 
    StructField("feature3",BooleanType(),True), 
  ])

pathParquet = "/tmp/parquetFiles"

# формирование dataframe
values= []
df = spark.createDataFrame(values,schema=schemaData)
# запишем пустые данные, необходимо для очистки
df.write.mode("overwrite").parquet(pathParquet)

schemaIndex = StructType([ \
    StructField("indx1",LongType(),True),
    StructField("indx2",LongType(),True),
  ])

# увеличиваем набор данных
batchSize = 30
labelCount = 10
feature1Count = 10 

def writeParquet():
    indx = list((idx,idx) for idx in range(batchSize))
    df = spark.createDataFrame(indx, schemaIndex)
    def extract_features(row):
        return (
            'label'+str(random.randint(1, labelCount)), #label
            random.randint(1, feature1Count), #feature1
            random.random(), #feature2
            bool(random.getrandbits(1)) , #feature3
        )
    rdd = df.rdd.map(extract_features)
    df = rdd.toDF( ["label","feature1","feature2", "feature3"])
    # запись в parquet
    df.write.mode("append").parquet(pathParquet)


# делаем некоторое количество пачек
for i in range(5):
    writeParquet()

localPathParquet = "/tmp/singleparquet"
dfSingle = spark.read.parquet(pathParquet)
fileCount = 1 # число файлов
dfSingle.coalesce(1).write.mode("overwrite").parquet(localPathParquet)

spark.stop()

import os
import boto3

# имя файла в s3
filePathParquet = "/tmp/dataset.parquet"
# имя корзины в s3
bucketNameParquet = 'data'

s3_target = boto3.resource('s3', 
    endpoint_url=os.environ["AWS_ENDPOINT_URL"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    aws_session_token=None,
    config=boto3.session.Config(signature_version='s3v4'),
    verify=False
)

# создание корзины
bucket = s3_target.Bucket(bucketNameParquet)
if (not bucket.creation_date):
   s3_target.create_bucket(Bucket=bucketNameParquet)

# загрузка файла на s3 
# в локальной папке находится единственный файл и закидывается на S3
fileNameParquetLocal = [x for x in os.listdir(localPathParquet) if x.endswith(".parquet")][0]
print('write to s3', 'backet='+bucketNameParquet, 'path='+filePathParquet)
s3_target.Bucket(bucketNameParquet).upload_file(localPathParquet+'/'+fileNameParquetLocal, filePathParquet)