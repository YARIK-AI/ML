# Подготовительные действия

## Настройка Docker

В разделе Settings во вкладке Kubernetes, включить опцию Enable Kubernetes

## Образы

Все необходимые скачивания образов выполняются при первом старте контейнеров, но можно (не обязательно), скачать образы последовательно вручную.

Для `docker` в `Windows`

```
docker pull aggrik/pyspark:latest
docker pull aggrik/greenplum_stable:latest
docker pull aggrik/minio:latest
docker pull aggrik/mlflow:latest
docker pull aggrik/postgresql:latest
docker pull aggrik/superset:latest
docker pull aggrik/tarantool:latest
docker pull aggrik/clickhouse:latest
```

Для `kubernetes` в `Linux`

```
sudo ctr -n=k8s.io image pull docker.io/aggrik/pyspark:latest
sudo ctr -n=k8s.io image pull docker.io/aggrik/greenplum_stable:latest
sudo ctr -n=k8s.io image pull docker.io/aggrik/minio:latest
sudo ctr -n=k8s.io image pull docker.io/aggrik/mlflow:latest
sudo ctr -n=k8s.io image pull docker.io/aggrik/postgresql:latest
sudo ctr -n=k8s.io image pull docker.io/aggrik/superset:latest
sudo ctr -n=k8s.io image pull docker.io/aggrik/tarantool:latest
sudo ctr -n=k8s.io image pull docker.io/aggrik/clickhouse:latest

```

# Запуск

Компоненты можно запускать отдельно, но есть некоторые зависимости: 

- mlflow зависит от minio
- mlflow зависит от postgres-mlflow
- superset зависит от postgres-superset

```
kubectl apply -f .\greenplum\
kubectl apply -f .\jupyter\
kubectl apply -f .\minio\
kubectl apply -f .\tarantool\
kubectl apply -f .\postgres-mlflow\
kubectl apply -f .\mlflow\
kubectl apply -f .\postgres-superset\
kubectl apply -f .\superset\
kubectl apply -f .\clickhouse\
```

# Удаление

```
kubectl delete -f .\greenplum\
kubectl delete -f .\jupyter\
kubectl delete -f .\minio\
kubectl delete -f .\tarantool\
kubectl delete -f .\postgres-mlflow\
kubectl delete -f .\mlflow\
kubectl delete -f .\postgres-superset\
kubectl delete -f .\superset\
kubectl delete -f .\clickhouse\
```

# Проверка работоспособности

## S3 

```
http://localhost:32010/
login - adminminio
passowrd - adminminio
```

## Jupyter

`http://localhost:31188/jupyter/?token=822fce15430e96de9bc18fedf9f938796db4c7927f912028`

## Clickhouse

http://localhost:32023/play
login - admin
passowrd - admin

# Перепределение сетевых портов

При необходимости можно переназначить сетевые порты на более привычные для соотвествующих сервисов. При переназначении высокий порт будет также доступен, но добавляется новый из более низкого диапазона. Для выполнения команды требуется запустить `Powershell` с правами администратора.

Прверить наличие открытых портов можно командой 'netstat -an'. Открытые порты будут в статусе `LISTENING`.

Для superset

```
# переназначить порт 32699 на 8088
netsh interface portproxy add v4tov4 protocol=tcp connectaddress=localhost connectport=32699 listenport=8088
# удалить назначение
netsh interface portproxy delete v4tov4 protocol=tcp listenport=8088
```

Для MLflow

```
# переназначить порт 32050 на 5000
netsh interface portproxy add v4tov4 protocol=tcp connectaddress=localhost connectport=32050 listenport=5000
# удалить назначение
netsh interface portproxy delete v4tov4 protocol=tcp listenport=5000
```

Для greenplum

```
# переназначить порт 31832 на 5432
netsh interface portproxy add v4tov4 protocol=tcp connectaddress=localhost connectport=31832 listenport=5432
# удалить назначение
netsh interface portproxy delete v4tov4 protocol=tcp listenport=5432
```

Для jupyter. C jupyter нужно внимательно перенаправлять порт, плагин под vscode может запустить версию jupyter и порт будет уже занят. И наоборот, если понадобится пользоваться встроенным jupyter не забудьте удалить переназначение порта.

```
# переназначить порт 31188 на 8888
netsh interface portproxy add v4tov4 protocol=tcp connectaddress=localhost connectport=31188 listenport=8888
# удалить назначение
netsh interface portproxy delete v4tov4 protocol=tcp listenport=8888
```

Для minio

```
# переназначить порт 32010 на 9001
netsh interface portproxy add v4tov4 protocol=tcp connectaddress=localhost connectport=32010 listenport=9001
netsh interface portproxy add v4tov4 protocol=tcp connectaddress=localhost connectport=32020 listenport=9000
# удалить назначение
netsh interface portproxy delete v4tov4 protocol=tcp listenport=9001
netsh interface portproxy delete v4tov4 protocol=tcp listenport=9000
```

Для clickhouse

```
# переназначить порт 32023 на 8123
netsh interface portproxy add v4tov4 protocol=tcp connectaddress=localhost connectport=32023 listenport=8123
# удалить назначение
netsh interface portproxy delete v4tov4 protocol=tcp listenport=8123