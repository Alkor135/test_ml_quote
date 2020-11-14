# -*- coding: utf-8 -*-
"""
Добавление колонки, является ли бар профитным при заданных ТП и СЛ
"""
import pandas as pd
import numpy as np
from pathlib import Path


def create_file_name_result(file_source, dir_result):
    """
    Создание имени выходного (результирующего) файла с путями
    :param file_source: Из имени файла который нужно обработать создаем имя выходного файла
    :param dir_result: Путь к выходному файлу
    :return: Имя выходного файла с путями
    """
    split_file_source_lst = file_source.split('.')  # Разобъем имя входного файла
    file_name_result = f'{split_file_source_lst[0]}.{split_file_source_lst[1]}_tpsl.csv'  # Соберем имя выходного файла
    return Path(f'{dir_result}/{file_name_result}')  # Соберем путь с именем


if __name__ == '__main__':
    dir_source = 'c:/data_prepare_quote_csv'  # Папка откуда берем csv файл для обработки
    file_source = 'SPFB.RTS_5min.csv'  # Исходный файл
    dir_result = 'c:/data_prepare_quote_csv'  # Папка куда складываем обработанный csv файл
    buy_tp = 500
    buy_sl = 500

    path_file_result = create_file_name_result(file_source, dir_result)  # Создаем имя выходного файла
    # print(path_file_result)

    # Загружаем файл в dataframe
    df_data = pd.read_csv(f'{dir_source}/{file_source}', delimiter=';', index_col='date_time')
    df_data[f'bay_{buy_tp}-{buy_sl}'] = np.nan  # Создание дополнительного столбца и заполнение его NaN
    # print(df_data)

    end_index = df_data.tail(1).index[0]  # Получаем индекс последней строки
    print(end_index)

    for index, row in df_data.iterrows():  # Перебираем строки dataframe df_data
        tpsl_value = np.nan  # Значение профитности бара устанавливаем в NaN
        tp_current_candle = row['close'] + buy_tp  # Рассчитываем уровень ТП текущего бара для покупок
        sl_current_candle = row['close'] - buy_sl  # Рассчитываем уровень СЛ текущего бара для покупок

        if end_index != index:  # Если индекс текущей строки не равен индексу последней строки
            df_next_row = df_data[index:].head(2)  # Создаем df из текущей строки и следующей
            next_index = df_next_row.index[1]  # Получаем индекс следующей строки
            df_next = df_data[next_index:]  # Создаем df из всех последующих строк (не включая текущую)
            for i, r in df_next.iterrows():  # Перебираем строки dataframe df_next
                if r['low'] <= sl_current_candle:
                    tpsl_value = 0
                    break
                elif r['high'] > tp_current_candle:
                    tpsl_value = 1
                    break
            df_data.loc[index, f'bay_{buy_tp}-{buy_sl}'] = tpsl_value
            # row[f'bay_{buy_tp}-{buy_sl}'] = tpsl_value
            # print(df_data[index: index])
            # print(row[f'bay_{buy_tp}-{buy_sl}'])
            print(index)
    print(df_data)
