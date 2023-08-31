import unittest

class TestClickhouse(unittest.TestCase):
    
    def test_create_database(self):
        import clickhouse_connect
        import os
        # подключение к системной базе данных
        HOST=os.environ['CLICKHOUSE_HOST']
        PORT=os.environ['CLICKHOUSE_PORT']
        DATABASE='default'
        LOGIN=os.environ['CLICKHOUSE_LOGIN']
        PASSWORD=os.environ['CLICKHOUSE_PASSWORD']
        # имя новой базы данных
        database_name = os.environ['CLICKHOUSE_DATABASE']
        connection = clickhouse_connect.get_client(host=HOST, 
                                            port=int(PORT), 
                                            database = "default",
                                            username=LOGIN, 
                                            password=PASSWORD,
                                            send_receive_timeout=12000,
                                            query_limit=0)
        sql = f"""
        create database if not exists {database_name}
        """
        result = connection.command(sql)
        sql = f"""
        SELECT count(name) FROM system.databases WHERE name = '{database_name}'
        """
        result = connection.command(sql)
        connection.close()        
        #количество баз данных
        self.assertEqual(result, 1)

    def test_create_table(self):
        tableName = 'table1'
        import clickhouse_connect
        import os
        # подключение к системной базе данных
        HOST=os.environ['CLICKHOUSE_HOST']
        PORT=os.environ['CLICKHOUSE_PORT']
        DATABASE=os.environ['CLICKHOUSE_DATABASE']
        LOGIN=os.environ['CLICKHOUSE_LOGIN']
        PASSWORD=os.environ['CLICKHOUSE_PASSWORD']
        connection = clickhouse_connect.get_client(host=HOST, 
                                            port=int(PORT), 
                                            database = "default",
                                            username=LOGIN, 
                                            password=PASSWORD,
                                            send_receive_timeout=12000,
                                            query_limit=0)
        # удаление базы данных
        sql = f"""
        drop table if exists {DATABASE}.{tableName}    
        """
        result = connection.command(sql)    
        # создание таблицы
        sql = f"""
        create table {DATABASE}.{tableName}
        (
            c1 int,
            c2 float,
            c3 varchar
        )
        ENGINE = MergeTree
        ORDER BY tuple()     
        """
        result = connection.command(sql)    
        sql = f"""
        SELECT count(name) FROM system.tables WHERE database = '{DATABASE}' and name = '{tableName}'
        """
        result = connection.command(sql)
        connection.close()        
        # количество таблиц
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)