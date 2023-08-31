import os
import boto3
import pandas

bucket_name = 'data'

s3_target = boto3.resource('s3', 
    endpoint_url=os.environ["AWS_ENDPOINT_URL"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    aws_session_token=None,
    config=boto3.session.Config(signature_version='s3v4'),
    verify=False
)

# чтение файла с s3 файла tmp/data.parquet в локальный файл 
localPath = '/tmp/data.parquet'
remotePath = 'tmp/dataset.parquet'
s3_target.Bucket(bucket_name).download_file(remotePath, localPath)

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, LongType, StringType, IntegerType, DateType, TimestampType, FloatType
from pyspark.sql.functions import col, cast, date_trunc, sum, dayofweek, hour, dayofmonth, lit, monotonically_increasing_id

# запуск spark
spark = SparkSession.builder.appName('fill').getOrCreate()

dfInput = spark.read.parquet(localPath)
df = dfInput.select(monotonically_increasing_id().alias('id'.upper()), 
                    col('label').alias('label'.upper()), 
                    col('feature1').alias('feature1'.upper()), 
                    col('feature2').alias('feature2'.upper()), 
                    col('feature3').alias('feature3'.upper()) ) 
df.printSchema

# подключение к БД Tarantool
HOST=os.environ['TARANTOOL_HOST']
PORT=os.environ['TARANTOOL_PORT']
LOGIN=os.environ['TARANTOOL_LOGIN']
PASSWORD=os.environ['TARANTOOL_PASSWORD']

# для tarantol необходимо создавать таблицу
tableName = 'dataset'

import tarantool
print("подключение к tarantool")
connection = tarantool.connect(host = HOST, port=PORT, user=LOGIN, password=PASSWORD)
table = tableName.upper()
# текст запроса на создание таблицы, поля в верхнем регистре
sqlCreateTable = f"""
create table {table} (  
    ID int primary key, 
    LABEL string, 
    FEATURE1 int, 
    FEATURE2 number, 
    FEATURE3 boolean 
)"""    

print("проверяется таблица:" + table)
rst = connection.execute(f"""SELECT EXISTS (select true from "_space" where "name" = '{table}')""")
tableExist = rst[0][0]
print('таблица'+tableName.upper()+' существует '+str(tableExist))
if tableExist: 
    print("удаляется таблица:"+tableName)
    connection.execute(f"drop table {table}")
print("запрос создания: "+sqlCreateTable)
connection.execute(sqlCreateTable)
print("создана таблица: "+table)
#создание дополнительного индекса
createIndexSQL = f'''CREATE INDEX {table}_label ON {table} (label)'''
print(createIndexSQL)
connection.execute(createIndexSQL)
#отключение
connection.close()

# заполняем таблицу
jdbcURLTarantool = f'jdbc:tarantool://{HOST}:{PORT}?user={LOGIN}&password={PASSWORD}'

df.write.format("jdbc").mode("append") \
              .option('url', jdbcURLTarantool) \
              .option('driver', 'org.tarantool.jdbc.SQLDriver') \
              .option("dbtable",tableName.upper()).save()

# спарк завершает работу
spark.stop()