# -*- coding: utf-8 -*-
"""
Читает файл csv с кодировкой по Лиховидову в DataFrame.
Строит график движения цены после выбранного кода.
"""
import pandas as pd
import numpy as np


if __name__ == '__main__':
    # Загружаем файл с разделителем ',' в DF
    df = pd.read_csv('c:\data_prepare_quote_csv\SPFB.RTS_5min_2020-09-01_2020-11-10_lihovidov.csv', delimiter=',')
    # Меняем индекс и делаем его типом datetime
    df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
    df = df.drop('date_time', axis=1)  # Удаляем колонку с датой и временем, т.к. дата-время у нас теперь в индексе
    # print(df)

    # Создаем DF с заданным кодом
    df_candle_code = df.query('candle_code == 0')
    # print(df_candle_code)

    # Перебираем строки DF df_candle_code
    for index, row in df_candle_code.iterrows():  # Перебираем строки dataframe df_candle_code
        df_posl = df[index:].head(20)  # Создаем последующий DF

        price_at_t0 = df_posl.iloc[0, 5]  # Берем самое первое по времени значение (к нему нормализуем)
        df_posl[index] = df_posl.apply(lambda row: row['close'] / price_at_t0, axis=1)  # axis=1 Указывает на колонку
        df_posl.reset_index()
        print(df_posl)


        break