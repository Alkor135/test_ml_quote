# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from datetime import datetime, time

if __name__ == '__main__':
    dir_source = 'c:/data_prepare_quote_csv'  # Папка откуда берем csv файл для обработки
    file_source = 'SPFB.RTS_5min.csv'  # Исходный файл

    # Загружаем файл в dataframe
    df_data = pd.read_csv(f'{dir_source}/{file_source}', delimiter=';', index_col='date_time')

    print(df_data.loc[df_data.index < '2020-01-03 10:10:00'])
    date_lst = ['2020-01-03', '2020-01-04']
    print(df_data.loc[df_data.index < f'{date_lst[0]} 10:10:00'])

    s = pd.Series(df_data.index).array
    print(s)
    date_list = []
    for i in s:
        date_one = i.split(' ')
        if not date_one[0] in date_list:
            date_list.append(date_one[0])
    print(date_list)

# print(pd.to_datetime('10:00:00', format='%H:%M:%S').datetime.time)
