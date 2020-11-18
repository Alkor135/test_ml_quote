# -*- coding: utf-8 -*-
import pandas as pd

# Загружаем файл в DF
df = pd.read_csv('c:/data_prepare_quote_csv/SPFB.RTS_5min.csv', delimiter=';', index_col='date_time')
# df = df[lambda x: x['time'] == 100000]
df = df.loc[df['time'] == 100000]
df['abs_body_condle'] = df.apply(lambda row: abs(row['open'] - row['close']), axis=1)  # axis=1 Указывает на колонку
# print(df)
# print(abs(-10))

print(df[['abs_body_condle']].mean())  # Среднее
