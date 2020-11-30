# -*- coding: utf-8 -*-
"""
Читает файл csv с кодировкой по Лиховидову в DataFrame.
Строит график движения цены после выбранного кода за заданные даты.
"""
import pandas as pd
import matplotlib.pyplot as plt
from itertools import groupby


def candle_code_graf(df, candlestik_code, month):
    # Создаем DF с заданным в переменной candlestik_code кодом
    df_candle_code = df.query(f'candle_code == {candlestik_code}')
    # print(df_candle_code.shape)
    # print(df_candle_code.index[0].date())
    # print(df_candle_code)

    df_graf = pd.DataFrame()  # Задаем пустой df куда будем писать значения закрытия свечей

    # Перебираем строки DF df_candle_code
    for index, row in df_candle_code.iterrows():  # Перебираем строки dataframe df_candle_code
        # print(str(index.date()))
        # Для создания последующего DF возьмем DF за дату index
        df_posl = df.loc[str(index.date())]
        # Оставим в DF только строки по времени index и до конца дня
        df_posl = df_posl.between_time(str(index.time()), '23:59:59')  # Создаем последующий DF

        # print(df_posl)
        # df_posl.to_excel('example.xlsx')
        # break

        # price_at_t0 = df_posl.iloc[0, 4]  # Берем самое первое по времени значение "close" (к нему нормализуем)
        close_t0 = df_posl.loc[index, 'close']  # Берем самое первое по времени значение "close" (к нему нормализуем)
        # print(close_t0)
        # break

        # В DF df_posl создаем новое поле с датой и временем из index и туда пишем нормализованные цены close
        df_posl[index] = df_posl.apply(lambda row: row['close'] / close_t0, axis=1)
        # Перезаписываем индекс простой последовательностью для слияния
        df_posl.reset_index(drop=True, inplace=True)
        # print(df_posl)
        # break

        # DF df_graf объединяем с полем df_posl[index] (index - теперь название поля в df_posl)
        df_graf = df_graf.join(df_posl[index], how='outer')  # Join с объединением ключей)
        # print(df_graf)
        # break

    # print(df_graf)

    # Строим график
    columns_lst = list(df_graf.columns)

    plt.figure(figsize=(19, 9))

    plt.title(f"RTS движение цены после свечи М5 за {month} с кодом по Лиховидову {int(candlestik_code)}")
    for column in columns_lst:
        df_graf[column].plot()
    plt.axhline(y=1.01, color='black', linestyle='-')
    plt.axhline(y=1.00, color='blue', linestyle='-')
    plt.axhline(y=0.99, color='black', linestyle='-')
    plt.savefig(f'c:/data_prepare_quote_csv/pic/{int(candlestik_code)}_{month}.png')
    # plt.show()
    plt.close()


if __name__ == '__main__':
    month = '2020-11'  # Месяц за который создаем картинки

    # Загружаем файл с разделителем ',' в DF
    # df = pd.read_csv('c:/data_prepare_quote_csv/SPFB.RTS_5min_2020-09-01_2020-11-10_lihovidov.csv', delimiter=',')
    df = pd.read_csv('c:/data_prepare_quote_csv/SPFB.RTS_5min_2020-01-03_2020-11-10_lihovidov.csv', delimiter=',')
    # Меняем индекс и делаем его типом datetime
    df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
    df = df.drop('date_time', axis=1)  # Удаляем колонку с датой и временем, т.к. дата-время у нас теперь в индексе
    df = df.drop('date', axis=1)  # Удаляем колонку с датой
    df = df.drop('time', axis=1)  # Удаляем колонку со временем
    df = df.loc[month]
    # print(df)

    tmp_lst = list(df['candle_code'])  # Создаем список с кодами свечей по Лиховидову
    tmp_lst.sort()  # Сортируем список с кодами свечей по Лиховидову
    candlestik_code_lst = [el for el, _ in groupby(tmp_lst)]  # Удаляем повторяющиеся элементы

    # print(candlestik_code_lst)

    for elem in candlestik_code_lst:  # Перебираем список с кодами по Лиховидову
        print(int(elem))
        candle_code_graf(df, elem, month)  # Вызываем
        # break
