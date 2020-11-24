# -*- coding: utf-8 -*-
"""
Отображает на графиках движение цены после первого бара (после 10:00 бара)
Графики отдельные для понижающейся и повашающейся первой свечи с фильтром по среднему значению, т.е.
для расчета берутся только свечи чье тело менше среднего значение тел первых свечей.
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt


def mean_first_candles():
    """
    Функция подсчитывает среднее значение для первых за сессию свечей
    :return:  Среднее значение для первых свечей за сессию (свечи в 10:00)
    """
    # Читаем в DF сводный файл
    df = pd.read_csv('c:/data_prepare_quote_csv/SPFB.RTS_5min.csv', delimiter=';', index_col='date_time')

    # Оставляем в DF только строки соотретствующие открытию сесии (10:00)
    df = df.loc[df['time'] == 100000]

    # Создаем новое поле 'abs_body_candle' куда записываем модуль разницы открытия и закрытия свечи
    df['abs_body_candle'] = df.apply(lambda row: abs(row['open'] - row['close']), axis=1)  # axis=1 Указывает на колонку

    return df[['abs_body_candle']].mean()  # Возвращаем среднее


def create_df_for_plot(files_lst):
    """
    Создает два dataframe для построения графиков движения цены после первой свечи с фильтром по среднему
    :param file_lst: Получает список файлов (по дням) для обработки
    :return: Возвращает два dataframe для повышающейся и понижающейся первой свечи с фильтром по среднему
    """
    df_up = pd.DataFrame()  # Задаем пустой df куда будем писать значения закрытия свечей после повышающейся свечи
    df_down = pd.DataFrame()  # Задаем пустой df куда будем писать значения закрытия свечей после понижающейся свечи

    # среднее по всем первым свечам
    candle_first_mean = float(mean_first_candles())

    # В цикле обрабатываем список файлов
    for file in files_lst:
        df = pd.read_csv(file, delimiter=',')  # Загружаем файл в DF

        # Дату в нужном формате строкой, она понадобиться для названия новой колонки с нормализованной ценой
        new_name_column = datetime.strptime(str(df.iat[0, 0]), '%Y%m%d').date()  # Дату в нужном формате строкой

        df = df.set_index(
            pd.to_datetime(df['<TIME>'], format='%H%M%S').dt.time)  # Меняем индекс и делаем его типом time

        # Берем самое первое по времени значение <CLOSE> к нему нормализуем цены <CLOSE> и заносим к новую колонку
        # с датой в имени
        price_at_t0 = df.iloc[0, 5]  # Берем самое первое по времени значение <CLOSE> (к нему нормализуем)
        df[new_name_column] = df.apply(lambda row: row['<CLOSE>'] / price_at_t0, axis=1)  # axis=1 Указывает на колонку

        if abs(df.iloc[0, 2] - df.iloc[0, 5]) < (candle_first_mean * 0.9):
            if df.iloc[0, 2] < df.iloc[0, 5]:  # Первая свеча на повышение (формируем df_up)

                df_up = df_up.join(df[new_name_column], how='outer')  # Join с объединением ключей
            else:
                df_down = df_down.join(df[new_name_column], how='outer')  # Join с объединением ключей

    # Сохраняем в файлы для проверки
    # df_up.to_excel('example_up.xlsx')
    # df_down.to_excel('example_down.xlsx')

    # Проверяем на пустые значения
    # print(df_up.isna().sum().sum())
    # print(df_down.isna().sum().sum())

    # Заполняем NaN предыдущими значениями и опять проверяем
    df_up.fillna(method='ffill', inplace=True)
    df_down.fillna(method='ffill', inplace=True)
    # print(df_up.isna().sum().sum())
    # print(df_down.isna().sum().sum())

    return df_up, df_down


if __name__ == '__main__':
    dir_source = Path('c:/data_finam_quote_csv')  # Папка откуда берем csv файлы для обработки
    file_mask = 'SPFB.RTS_5min_*.csv'  # Маска файлов, которые обрабатываем

    files_lst = list(dir_source.glob(file_mask))  # Создаем список файлов которые будем обрабатывать

    df_up, df_down = create_df_for_plot(files_lst)  # Создаем df'ы для построения графиков

    # Строим график
    columns_lst_up = list(df_up.columns)
    # print(columns_lst_up)
    plt.title("RTS движение цены после первой повышающейся свечи М5 за 2020 с фильтром по среднему значению")
    for column in columns_lst_up:
        df_up[column].plot()
    plt.axhline(y=1.025, color='black', linestyle='-', label='+2,5%')
    plt.axhline(y=0.975, color='black', linestyle='-', label='-2,5%')
    plt.show()

    # Строим график
    columns_lst_down = list(df_down.columns)  # Создаем список колонок dataframe df_down
    # print(columns_lst_down)
    plt.title("RTS движение цены после первой понижающейся свечи М5 за 2020 с фильтром по среднему значению")
    for column in columns_lst_down:
        df_down[column].plot()
    plt.axhline(y=1.025, color='black', linestyle='-')
    plt.axhline(y=0.975, color='black', linestyle='-')
    plt.show()
