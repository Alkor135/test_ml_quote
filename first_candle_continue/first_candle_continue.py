# -*- coding: utf-8 -*-
"""
Отображает на графике движение цены после 0 бара (после 10:00 бара)
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt


def normalize_close_value(df, new_name_column):
    price_at_t0 = df.iloc[0, 5]  # Берем самое первое по времени значение (к нему нормализуем)
    df[new_name_column] = df.apply(lambda row: row['<CLOSE>'] / price_at_t0, axis=1)  # axis=1 Указывает на колонку
    return df


def get_row_file(file_name):
    """
    Из файла делает df с ценами закрытия свечей
    :param file_name: Получает в аргументе название файла для обработки
    :return: Возвращает df в виде строки цен закрытия (в индексе дата, названия колонок - время)
    """
    df = pd.read_csv(file_name, delimiter=',')  # Загружаем файл в DF
    # Дату в нужном формате (строкой) для смены названия колонки <CLOSE>
    new_name_column = datetime.strptime(str(df.iat[0, 0]), '%Y%m%d').date()  # Дату в нужном формате строкой
    df = df.set_index(pd.to_datetime(df['<TIME>'], format='%H%M%S').dt.time)  # Меняем индекс и делаем его типом time

    normalize_close_value(df, new_name_column)

    # df.columns = [new_name_column if x == '<CLOSE>' else x for x in df.columns]  # Меняем название колонки <CLOSE>
    # df = df[1:]  # Сохраняем без перврвой строки который в 10:00

    df_transposed = df.transpose()  # Транспонируем
    df = df_transposed[new_name_column:new_name_column]  # Выбираем нужную строку (бывшую <CLOSE>) и её в df
    return df


if __name__ == '__main__':
    dir_source = Path('c:/data_finam_quote_csv')  # Папка откуда берем csv файлы для обработки
    file_mask = 'SPFB.RTS_5min_*.csv'  # Маска файлов, которые обрабатываем

    files_lst = list(dir_source.glob(file_mask))  # Создаем список файлов которые будем обрабатывать

    df = pd.DataFrame()  # Задаем пустой df куда будем писать значения закрытия свечей
    for file in files_lst:
        df = df.combine_first(get_row_file(file))  # Слияние двух dataframe
        # break
    print(df)

    df = df.set_index(df['<TIME>'])  # Меняем индекс на '<TIME>'
    print(df)

    # df.to_excel('example.xlsx')

    # Строим график в виде гистограммы
    df.plot(df.iloc[1])
    plt.show()
