import airflow
from airflow import DAG
from pendulum import datetime
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow import configuration as conf
from airflow.utils.dates import days_ago
import os

## Вариант без авторизации
fileName = 'df_show.py'
gitFileUrl = 'https://raw.githubusercontent.com/YARIK-AI/ML/main/docs/examples/pyspark/'+ fileName
header = ""

## Вариант с авторизацией
# получить персональный токен для доступа к github
# ссылка на инструкцию
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic
# ссылка на создание токена
# https://github.com/settings/tokens


with DAG(
    dag_id="get_file",
    schedule_interval=None,
    is_paused_upon_creation=True,
    start_date=  airflow.utils.dates.days_ago(0),
    catchup=False,
    max_active_runs=1,
) as dag: 

  namespace = conf.get('kubernetes', 'NAMESPACE')    

  runPython = KubernetesPodOperator(
      task_id="task_id_python",
      name="task_name_python",
      namespace=namespace,
      image=os.environ['IMAGE_NAME_PYSPARK'],
      # --- команда внутри контейнера ---
      cmds=["/bin/bash", "-c"],
      arguments=[f"""wget {header} -O {fileName} -q {gitFileUrl} \
                 && python {fileName}
                 """],
      image_pull_policy="IfNotPresent",
      # ------
      labels={"app": "app1"},
      startup_timeout_seconds=240,
      get_logs=True,
      random_name_suffix=False,
      is_delete_operator_pod=True)

if __name__ == "__main__":
    dag.test()