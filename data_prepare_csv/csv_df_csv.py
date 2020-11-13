# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path


def columns_change(df):
    """
    Функция меняет заголовок полученного в аргументе dataframe.
    Убирает лишние символы (<, >)
    Приводит названия к нижнему регистру
    :param df:
    :return:
    """
    title_lst = df.columns.values  # Создаем список с названиями заголовков принятого в аргументе dataframe
    # В списке title_lst_new будут новые названия колонок
    title_lst_new = [x.replace('<', '') for x in title_lst]  # Удаляем символ '<' в каждом элементе списка
    title_lst_new = [x.replace('>', '') for x in title_lst_new]  # Удаляем символ '>' в каждом элементе списка
    title_lst_new = [x.lower() for x in title_lst_new]  # Приводим список с новыми заголовками к нижнему регистру
    rename_dic = dict(zip(title_lst, title_lst_new))  # Создаем словарь для переименования заголовка
    df = df.rename(columns=rename_dic)
    return df


def date_time_join(df):
    """
    Функция добавляет колонку date_time методом слияния <DATE> и <TIME>, и делает её индексом
    :param df: На вход получаем dataframe
    :return: Возвращаем измененый dataframe
    """
    df['date_time'] = df['<DATE>'].astype(str) + ' ' + df['<TIME>'].astype(str)  # Слияние столбцов в поле date_time
    df = df.set_index(pd.DatetimeIndex(df['date_time']))  # Меняем индекс и делаем его типом date
    df = df.drop('date_time', 1)  # Удаляем ненужную колонку. 1 означает, что отбрасываем колонку а не индекс
    return df


def create_file_name_result(file_mask):
    """
    Создание имени выходного (результирующего) файла с путями
    :param file_mask: Из маски файлов которые нужно обработать создаем имя выходного файла
    :return: Имя выходного файла с путями
    """
    split_file_mask_lst = file_mask.split('_')  # Разобъем маску входных файлов
    file_name_result = f'{split_file_mask_lst[0]}_{split_file_mask_lst[1]}.csv'  # Соберем имя выходного файла
    return Path(f'{str(dir_result)}/{file_name_result}')  # Соберем путь с именем


if __name__ == '__main__':
    dir_source = Path('c:/data_finam_quote_csv')  # Папка откуда берем csv файлы для обработки
    dir_result = Path('c:/data_prepare_quote_csv')  # Папка куда складываем обработанные csv файлы
    file_mask = 'SPFB.RTS_5min_*.csv'  # Маска файлов, которые обрабатываем

    if not dir_result.exists():  # Если результирующей папки не существует
        Path.mkdir(dir_result)  # Создаем папку куда положим обработанный файл

    path_file_result = create_file_name_result(file_mask)  # Создание имени результирующего файла
    print(path_file_result)

    if not path_file_result.exists():  # Если результирующего файла не существует
        # Создаем пустой dataframe в который будем добавлять dataframe из прочитанных файлов (обработанные)
        df_res = pd.DataFrame()
    else:
        # Читаем csv файл в dataframe
        df_res = pd.read_csv(str(path_file_result), delimiter=';', index_col='date_time')
    print(df_res)

    file_lst = list(dir_source.glob(file_mask))  # Создаем список файлов которые будем обрабатывать
    for file in file_lst:
        df_quote = pd.read_csv(file, delimiter=',')  # Загружаем файл в DF
        df_quote = date_time_join(df_quote)  # Меняем индекс в dataframe на дату и время
        df_quote = columns_change(df_quote)  # Меняем названия колонок
        df_res = df_res.combine_first(df_quote)  # Слияние двух dataframe
    print(df_res)
    df_res.to_csv(str(path_file_result), sep=';', index_label='date_time')
