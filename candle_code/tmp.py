# -*- coding: utf-8 -*-

import pandas as pd


df = pd.read_csv('c:/data_prepare_quote_csv/SPFB.RTS_5min.csv', delimiter=';')
df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))  # Меняем индекс и делаем его типом datetime
df = df.drop('date_time', 1)  # Удаляем колонку с датой, т.к. дата у нас теперь в индексе

df_row = df.iloc[[0]]  # Одна строка DF получена по индексу
date = df_row.index.date  # Индекс в виде даты
time = df_row.index.time  # Индекс в виде времени

print(df_row)
print(date)
print(time)

# date_str = date[0].strftime("%Y-%m-%d")
# print(date_str)

res_df = df.loc[date[0].strftime("%Y-%m-%d")]
print(res_df)
