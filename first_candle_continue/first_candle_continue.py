# -*- coding: utf-8 -*-
"""
Отображает на графике движение цены после 0 бара (после 10:00 бара)
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt



if __name__ == '__main__':
    dir_source = Path('c:/data_finam_quote_csv')  # Папка откуда берем csv файлы для обработки
    file_mask = 'SPFB.RTS_5min_*.csv'  # Маска файлов, которые обрабатываем

    file_lst = list(dir_source.glob(file_mask))  # Создаем список файлов которые будем обрабатывать
    df = pd.read_csv(file_lst[1], delimiter=',')  # Загружаем файл в DF
    # print(df)

    new_name_column = datetime.strptime(str(df.iat[0, 0]), '%Y%m%d').date()  # Дата в нужном формате строкой
    print(new_name_column)

    df = df.set_index(pd.to_datetime(df['<TIME>'], format='%H%M%S').dt.time)  # Меняем индекс и делаем его типом time
    df.columns = [new_name_column if x == '<CLOSE>' else x for x in df.columns]  # Меняем название колонки <CLOSE>

    df = df[1:]  # Сохраняем без перврго столбца который в 10:00
    df_transposed = df.transpose()  # Транспонируем

    print(df_transposed)
    df = df_transposed[new_name_column:new_name_column]  # Выбираем нужную строку и её в df
    print(df)




