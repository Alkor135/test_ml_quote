# -*- coding: utf-8 -*-
"""
Строит графики из csv
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


if __name__ == '__main__':
    path_dir = Path('c:/data_prepare_quote_csv/')  # Путь до каталога
    file_mask = 'graf_*.csv'  # Файл
    files_lst = list(path_dir.glob(file_mask))  # Список файлов

    for file in files_lst:
        df = pd.read_csv(f'{file}', index_col='index')  # Читаем файл в df
        # Строим график
        columns_lst = list(df.columns)
        plt.figure(figsize=(19, 9))

        plt.title(f"RTS движение цены после свечи М5 с кодом по Лиховидову {file}")
        for column in columns_lst:
            df[column].plot()
        plt.axhline(y=0.01, color='black', linestyle='-')
        plt.axhline(y=0.00, color='blue', linestyle='-')
        plt.axhline(y=-0.01, color='black', linestyle='-')
        plt.legend()
        plt.savefig(f'{file}.png')
        # plt.show()
        plt.close()
