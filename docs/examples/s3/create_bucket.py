import os
import boto3

bucket_name = 'mldata'

# адрес сервера, логин и пароль беруться из пременных окружения 
# переменные окружения уже установлены AWS_ENDPOINT_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
s3_target = boto3.resource('s3', 
    endpoint_url=os.environ["AWS_ENDPOINT_URL"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    aws_session_token=None,
    config=boto3.session.Config(signature_version='s3v4'),
    verify=False
)

# создание корзины
s3_target.create_bucket(Bucket=bucket_name)

# создание тестового файла
import pandas as pd

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)
df.to_parquet('/tmp/data.parquet')
df

# загрузка файла на s3 в tmp/data.parquet
s3_target.Bucket(bucket_name).upload_file('/tmp/data.parquet', 'tmp/data.parquet')

# чтение файла с s3 файла tmp/data.parquet в локальный файл /tmp/data1.parquet
s3_target.Bucket(bucket_name).download_file('tmp/data.parquet', '/tmp/data1.parquet')

# проверяем, считываем локальный файл
df1 = pd.read_parquet('/tmp/data1.parquet')
df1