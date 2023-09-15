# Инструкция по просмотру записей kafka

Для подключения к kafka используется иструмент "Offset Explorer" (https://www.kafkatool.com/).

1) Скачайте и установите программу
2) Запустите компонент Очередь сообщений

```bash
kubectl apply -f ./zookeeper
kubectl apply -f ./kafka/
```

3) Запустите программу "Offset Explorer", на главном окне для объекта Clusters откройте контекстное меню, выберите пункт "Import Connections ..."
4) Выполните импорт файла 'docs\examples\Offset Explorer\YARIK_connection_backup.xml'
5) Откройте соединение YARIK