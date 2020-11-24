# -*- coding: utf-8 -*-
"""
Читает файл csv в DataFrame. Добавляет колонку с кодом свечи.
"""
import pandas as pd
import numpy as np


def candle_value(previous_df):
    for index, row in previous_df.iterrows():  # Перебираем строки dataframe previous_df
        if row['open'] > row['close']:  # Свеча на понижение
            previous_df.loc[index, 'shadow_high'] = row['high'] - row['open']
            previous_df.loc[index, 'shadow_low'] = row['close'] - row['low']
            previous_df.loc[index, 'candle_body'] = row['open'] - row['close']
        else:
            previous_df.loc[index, 'shadow_high'] = row['high'] - row['close']
            previous_df.loc[index, 'shadow_low'] = row['open'] - row['low']
            previous_df.loc[index, 'candle_body'] = row['close'] - row['open']

        # print(previous_df)
        # print(row['open'])
        # print(row['close'])
        # print(row['high'])
        # print(row['low'])
        # break
    previous_df.to_excel('example.xlsx')


if __name__ == '__main__':
    dir_source = 'c:/data_prepare_quote_csv'  # Папка откуда берем csv файл для обработки
    file_source = 'SPFB.RTS_5min.csv'  # Исходный файл
    dir_result = 'c:/data_prepare_quote_csv'  # Папка куда складываем обработанный csv файл
    start_date = '2020-09-01'  # С какой даты будем строить DF с кодами свечей
    day_delta = 365  # Дельта в днях для расчета показателей (большой, средний, маленький). Предшествует start_date

    df = pd.read_csv(f'{dir_source}/{file_source}', delimiter=';')  # Загружаем файл в DF
    # Меняем индекс и делаем его типом datetime
    df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
    df = df.drop('date_time', 1)  # Удаляем колонку с датой и временем, т.к. дата и время у нас теперь в индексе
    # print(df)

    df_candle_code = df.copy()  # Создаем копию DF, исключение предупреждений
    df_candle_code = df_candle_code.loc[start_date:]  # Срез DF в котором будет дополнительная колонка с кодами свечей
    df_candle_code['candle_code'] = np.nan  # Создание дополнительного столбца и заполнение его NaN
    # print(df_candle_code)

    for index, row in df_candle_code.iterrows():  # Перебираем строки dataframe df_candle_code
        # print(index.date())
        delta_day = pd.to_timedelta(f'{day_delta} days')  # Преобразование типа
        # print(delta_day)
        start_previous_df = index.date() - delta_day  # Вычисляем начальную дату DF
        # print(start_previous_df)
        end_previous_df = index.date() - pd.to_timedelta('1 days')  # Вычисляем конечную дату DF
        # print(end_previous_df)
        # Создаем DF предшествующий текущей строке
        previous_df = df.loc[start_previous_df.strftime("%Y-%m-%d"): end_previous_df.strftime("%Y-%m-%d")]
        # print(previous_df)
        # print(index.time())
        previous_df = previous_df.loc[index.time()]  # Оставляем только строки соответствующие времени тек. строки
        # print(previous_df)
        candle_value(previous_df)
        break
