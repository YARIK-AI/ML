# В этом примере выполняется задача Airflow с использованием BashOpertor
# В задаче скачивается пример dag для airflow из github и устанавливается в airflow
# после успешного выполнения, будет доступна ссылка на dag, адрес http://localhost:32088/dags/example_EmptyOperator
# airflow требуется некоторое время на обновление списка задач (несколько минут)

import airflow
from airflow import DAG
from pendulum import datetime
from airflow.operators.bash_operator import BashOperator
from airflow import configuration as conf
from airflow.utils.dates import days_ago
import os

## Вариант без авторизации
fileName = 'dag_EmptyOperator.py'
gitFileUrl = f'https://raw.githubusercontent.com/YARIK-AI/ML/main/docs/examples/airflow/'+ fileName
header = ""

## Вариант с авторизацией
# получить персональный токен для доступа к github
# ссылка на инструкцию
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic
# ссылка на создание токена
# https://github.com/settings/tokens

#token = 'ghp_xТОКЕН' 
#fileName = '<имя файла>.py'
#gitFileUrl = 'https://raw.githubusercontent.com/<организация>/<проект>/master/<путь до файла>/'+ fileName
#header = f" --header 'Authorization: token {token}' "

with DAG(
    dag_id="example_BashOperator",
    schedule_interval=None,
    is_paused_upon_creation=True,
    start_date=  airflow.utils.dates.days_ago(0),
    catchup=False,
    max_active_runs=1,
) as dag:

  namespace = conf.get('kubernetes', 'NAMESPACE')    

  cmd = BashOperator(
    task_id='task_id',
    bash_command=f"wget --no-check-certificate {header} -O {os.environ.get('AIRFLOW__CORE__DAGS_FOLDER')+'/'+fileName} -q {gitFileUrl}"
  )

if __name__ == "__main__":
    dag.test()