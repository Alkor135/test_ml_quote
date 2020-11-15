# -*- coding: utf-8 -*-
"""
Показывает в виде графика гистограммы дневные экстремумы.
Использует файлы по дням
"""
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def prepare_df(df):
    """
    Подготавливает df для подсчета экстремумов
    :param df: Получает на вход df
    :return: Возвращает обработанный df
    """
    df['<TIME>'] = pd.to_datetime(df['<TIME>'], format='%H%M%S').dt.time  # Меняем тип поля '<TIME>'
    df = df.set_index(df['<TIME>'])  # Меняем индекс на '<TIME>'

    # Удаляем ненужные колонки. axis=1 означает, что удаляем колонку
    df = df.drop(['<TIME>', '<DATE>', '<OPEN>', '<CLOSE>', '<VOL>'], axis=1)
    return df


def create_df_for_plot(file_lst):
    """
    Создает dataframe для построения графика экстремумов по времени
    :param file_lst: Получает список файлов (по дням) для обработки
    :return: Возвращает dataframe с экстремумами (частота экстремумом в определенное время)
    """
    extremum_dic = {}  # Создаем словарь где будем подсчитывать экстремумы, ключами будет время
    for file in file_lst:  # Проходимся по списку файлов
        df_quote = pd.read_csv(file, delimiter=',')  # Загружаем файл в DF

        df_quote = prepare_df(df_quote)  # Обработка (подготовка) df

        max_time = df_quote['<HIGH>'].idxmax()  # Определяем индекс(время) максимума
        min_time = df_quote['<LOW>'].idxmin()  # Определяем индекс(время) минимума

        # Записываем макс и мин в словарь
        if max_time in extremum_dic:
            extremum_dic[max_time][0] += 1
        else:
            extremum_dic[max_time] = [1, 0]
        if min_time in extremum_dic:
            extremum_dic[min_time][1] += 1
        else:
            extremum_dic[min_time] = [0, 1]

    df = pd.DataFrame.from_dict(extremum_dic, orient='index', columns=['max', 'min'])  # Создаем df из словаря
    df.sort_index(inplace=True)  # Сортируем df по индексу (по времени)
    return df


if __name__ == '__main__':
    dir_source = Path('c:/data_finam_quote_csv')  # Папка откуда берем csv файлы для обработки
    file_mask = 'SPFB.RTS_5min_*.csv'  # Маска файлов, которые обрабатываем

    file_lst = list(dir_source.glob(file_mask))  # Создаем список файлов которые будем обрабатывать
    df = create_df_for_plot(file_lst)  # Создаем df для построения графика
    # print(df)
    print(df[max].sum)
    # print(df.sum(df[max]))

    # Строим график в виде гистограммы
    # index = df.index
    # df.plot(kind='bar')
    # plt.show()
