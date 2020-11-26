# -*- coding: utf-8 -*-
"""
Читает файл csv с кодировкой по Лиховидову в DataFrame.
Строит график движения цены после выбранного кода.
"""
import pandas as pd
import matplotlib.pyplot as plt
from itertools import groupby
# plt.figure(figsize=(19, 9))


def candle_code_graf(df, candlestik_code):
    # Создаем DF с заданным в переменной candlestik_code кодом
    df_candle_code = df.query(f'candle_code == {candlestik_code}')
    # print(df_candle_code.shape)
    # print(df_candle_code.index[0].date())
    # print(df_candle_code)

    df_graf = pd.DataFrame()  # Задаем пустой df куда будем писать значения закрытия свечей

    # Перебираем строки DF df_candle_code
    for index, row in df_candle_code.iterrows():  # Перебираем строки dataframe df_candle_code
        df_posl = df[index:].head(500)  # Создаем последующий DF
        # Переведем дату индекса нулевой строки последующего DF в строковый формат
        str_date = str(df_posl.index[0].date())
        # В последующем DF оставим только строки с датой изучаемой свечи, DF только за текущий день
        df_posl = df_posl.loc[str_date]
        # print(df_posl)

        price_at_t0 = df_posl.iloc[0, 5]  # Берем самое первое по времени значение (к нему нормализуем)
        df_posl[index] = df_posl.apply(lambda row: row['close'] / price_at_t0, axis=1)  # axis=1 Указывает на колонку
        # df_posl.reset_index(inplace=True)
        df_posl.reset_index(drop=True, inplace=True)

        df_graf = df_graf.join(df_posl[index], how='outer')  # Join с объединением ключей)

    # print(df_graf)

    # Строим график
    columns_lst = list(df_graf.columns)

    plt.figure(figsize=(19, 9))

    plt.title(f"RTS движение цены после свечи М5 с кодом по Лиховидову {candlestik_code}")
    for column in columns_lst:
        df_graf[column].plot()
    plt.axhline(y=1.01, color='black', linestyle='-')
    plt.axhline(y=1.00, color='blue', linestyle='-')
    plt.axhline(y=0.99, color='black', linestyle='-')
    plt.savefig(f'c:\data_prepare_quote_csv\pic\{candlestik_code}.png')
    # plt.show()


if __name__ == '__main__':
    # candlestik_code = 7  # Код свечи по лиховидову, к которой строим график
    # count_candle = 20

    # Загружаем файл с разделителем ',' в DF
    df = pd.read_csv('c:\data_prepare_quote_csv\SPFB.RTS_5min_2020-09-01_2020-11-10_lihovidov.csv', delimiter=',')
    # Меняем индекс и делаем его типом datetime
    df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
    df = df.drop('date_time', axis=1)  # Удаляем колонку с датой и временем, т.к. дата-время у нас теперь в индексе
    # print(df)

    tmp_lst = list(df['candle_code'])  # Создаем список с кодами свечей по Лиховидову
    tmp_lst.sort()  # Сортируем список с кодами свечей по Лиховидову
    candlestik_code_lst = [el for el, _ in groupby(tmp_lst)]  # Удаляем повторяющиеся элементы

    # print(candlestik_code_lst)

    for elem in candlestik_code_lst:  # Перебираем список с кодами по Лиховидову
        candle_code_graf(df, elem)  # Вызываем
        print(elem)
