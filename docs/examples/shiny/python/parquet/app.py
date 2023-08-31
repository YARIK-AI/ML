import pathlib
import pandas as pd
from shiny import App, Inputs, Outputs, Session, render, ui

# создание тестового набора данных
# для того, что бы пример работал независимо от других примеров, в нем создается набор данных
# это утяжеляет первичную зарузку, но дает возможность запускать пример в один клик
import createDataset


# загрузка данных
import loadDataset

import tarantool
import os
import pandas

tableName = 'dataset'

# подключение к БД Tarantool
HOST=os.environ['TARANTOOL_HOST']
PORT=os.environ['TARANTOOL_PORT']
LOGIN=os.environ['TARANTOOL_LOGIN']
PASSWORD=os.environ['TARANTOOL_PASSWORD']

# открытие соединения
connection = tarantool.connect(host = HOST, port=int(PORT), user=LOGIN, password=PASSWORD)

sql = f"""
SELECT distinct LABEL from {tableName.upper()}
order by LABEL
"""
rst = connection.execute(sql)
lstLabel = [x for rst in rst for x in rst]

sql = f"""
SELECT ID, LABEL, FEATURE1, FEATURE2, FEATURE3 from {tableName.upper()}
where 1=0
"""
rst = connection.execute(sql)
pdf = pandas.DataFrame( rst, columns=['ID', 'LABEL', 'FEATURE1', 'FEATURE2', 'FEATURE3'])
# обязательное закрытие соединения
connection.close()

app_ui = ui.page_fluid(
    ui.input_select("sliderLabel", None, lstLabel),
    ui.output_table("result")
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.table
    def result():

        # открытие соединения
        connection = tarantool.connect(host = HOST, port=int(PORT), user=LOGIN, password=PASSWORD)

        sql = f"""
        SELECT ID, LABEL, FEATURE1, FEATURE2, FEATURE3 from {tableName.upper()}
        where label = '{str(input.sliderLabel())}'
        """
        rst = connection.execute(sql)
        pdf = pandas.DataFrame( rst, columns=['ID', 'LABEL', 'FEATURE1', 'FEATURE2', 'FEATURE3'])
        # обязательное закрытие соединения
        connection.close()

        return pdf

app = App(app_ui, server)

