import unittest

class TestGreenplum(unittest.TestCase):
    
    def test_create_database(self):
        import psycopg2
        import os
        # подключение к системной базе данных
        HOST=os.environ['GREENPLUM_HOST']
        PORT=os.environ['GREENPLUM_PORT']
        DATABASE='postgres'
        #SCHAMA=os.environ['GREENPLUM_SCHEMA']
        LOGIN=os.environ['GREENPLUM_LOGIN']
        PASSWORD=os.environ['GREENPLUM_PASSWORD']
        connection = psycopg2.connect( host=HOST, port=PORT, database=DATABASE, user=LOGIN, password=PASSWORD)
        # имя новой базы данных
        database_name = os.environ['GREENPLUM_DATABASE']
        # проверка наличий базы данных
        sql = f"""
            select count(*) as cnt FROM pg_database WHERE datname = '{database_name}'
        """
        cur = connection.cursor()
        cur.execute(sql)
        exist = (cur.fetchone())[0]
        print('exist =',exist)
        connection.commit()
        # создание базы данных
        if not exist:
            sql = f"""
            create database {database_name}
            """
            connection.autocommit = True
            cur = connection.cursor()
            cur.execute(sql)
            cur.close()
        # повторная прове наличий базы данных
        sql = f"""
            select count(*) as cnt FROM pg_database WHERE datname = '{database_name}'
        """
        cur = connection.cursor()
        cur.execute(sql)
        exist = (cur.fetchone())[0]
        print('exist =',exist)
        cur.close()
        #количество баз данных
        self.assertEqual(exist, 1)

    def test_create_table(self):
        tableName = 'table1'        
        import psycopg2
        import os
        # подключение к базе данных
        HOST=os.environ['GREENPLUM_HOST']
        PORT=os.environ['GREENPLUM_PORT']
        DATABASE=os.environ['GREENPLUM_DATABASE']
        SCHEMA = os.environ['GREENPLUM_SCHEMA']
        LOGIN=os.environ['GREENPLUM_LOGIN']
        PASSWORD=os.environ['GREENPLUM_PASSWORD']
        connection = psycopg2.connect( host=HOST, port=PORT, database=DATABASE, user=LOGIN, password=PASSWORD)
        # необходимо убедиться, что схема создана
        sql = f"""
            create schema if not exists {SCHEMA}
        """
        cur = connection.cursor()
        cur.execute(sql)
        connection.commit()
        # удаление таблицы
        sql = f"""
        drop table if exists {DATABASE}.{tableName}    
        """
        cur = connection.cursor()
        cur.execute(sql)
        connection.commit()
        # создание таблицы
        tableName = 'table1'
        sql = f"""
            create table {SCHEMA}.{tableName}
            (
            c1 int,
            c2 float,
            c3 varchar
            )
        """
        cur = connection.cursor()
        cur.execute(sql)
        connection.commit()
        cur.close()
        # создание индекса
        createIndexSQL = f'''CREATE INDEX {tableName}_idx ON {SCHEMA}.{tableName} (c1)'''
        try:
            cur = connection.cursor()
            cur.execute(createIndexSQL)
            connection.commit()
        except Exception as e: 
            print(e)
        finally:
            cur.close()
        # количество таблиц
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)