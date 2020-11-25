# -*- coding: utf-8 -*-
"""
Читает файл csv в DataFrame. Добавляет колонку с кодом свечи по Лиховидову.
Расчет (большой, средний, маленький) ведется по свечам тогоже времени за предшествующие дни.
Количество предшествующих дней выбирается. Нужно предусмотреть csv файл с большей историей чем start_date на day_delta
"""
import pandas as pd
import numpy as np


def candle_value(previous_df):
    percentile_dic = {}
    for index, row in previous_df.iterrows():  # Перебираем строки dataframe previous_df
        if row['open'] > row['close']:  # Свеча на понижение
            previous_df.loc[index, 'shadow_high'] = row['high'] - row['open']
            previous_df.loc[index, 'shadow_low'] = row['close'] - row['low']
            previous_df.loc[index, 'candle_body'] = row['open'] - row['close']
        else:
            previous_df.loc[index, 'shadow_high'] = row['high'] - row['close']
            previous_df.loc[index, 'shadow_low'] = row['open'] - row['low']
            previous_df.loc[index, 'candle_body'] = row['close'] - row['open']

    percentile_dic['shadow_high_33'] = np.percentile(previous_df['shadow_high'], 33)
    percentile_dic['shadow_high_66'] = np.percentile(previous_df['shadow_high'], 66)
    percentile_dic['shadow_low_33'] = np.percentile(previous_df['shadow_low'], 33)
    percentile_dic['shadow_low_66'] = np.percentile(previous_df['shadow_low'], 66)
    percentile_dic['candle_body_33'] = np.percentile(previous_df['candle_body'], 33)
    percentile_dic['candle_body_66'] = np.percentile(previous_df['candle_body'], 66)

    return percentile_dic


if __name__ == '__main__':
    dir_source = 'c:/data_prepare_quote_csv'  # Папка откуда берем csv файл для обработки
    file_source = 'SPFB.RTS_5min.csv'  # Исходный файл
    dir_result = 'c:/data_prepare_quote_csv'  # Папка куда складываем обработанный csv файл
    start_date = '2020-09-01'  # С какой даты будем строить DF с кодами свечей
    day_delta = 365  # Дельта в днях для расчета показателей (большой, средний, маленький). Предшествует start_date

    df = pd.read_csv(f'{dir_source}/{file_source}', delimiter=';')  # Загружаем файл в DF
    # Меняем индекс и делаем его типом datetime
    df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
    df = df.drop('date_time', 1)  # Удаляем колонку с датой и временем, т.к. дата и время у нас теперь в индексе
    # print(df)

    df_candle_code = df.copy()  # Создаем копию DF, исключение предупреждений
    df_candle_code = df_candle_code.loc[start_date:]  # Срез DF в котором будет дополнительная колонка с кодами свечей
    df_candle_code['candle_code'] = np.nan  # Создание дополнительного столбца и заполнение его NaN
    # print(df_candle_code)

    for index, row in df_candle_code.iterrows():  # Перебираем строки dataframe df_candle_code
        print()
        print(index)
        delta_day = pd.to_timedelta(f'{day_delta} days')  # Преобразование типа
        start_previous_df = index.date() - delta_day  # Вычисляем начальную дату DF
        end_previous_df = index.date() - pd.to_timedelta('1 days')  # Вычисляем конечную дату DF
        # Создаем DF предшествующий текущей строке
        previous_df = df.loc[start_previous_df.strftime("%Y-%m-%d"): end_previous_df.strftime("%Y-%m-%d")]
        previous_df = previous_df.loc[index.time()]  # Оставляем только строки соответствующие времени тек. строки
        percentile_dic = candle_value(previous_df)

        # print(percentile_dic)
        code_str = ''  # Строка в которую будем собирать код для текущей свечи

        # Свеча на понижение (медвежья)
        if row['open'] > row['close']:  # Свеча на понижение (медвежья)
            code_str += '0'
            # Для тела медвежьей свечи
            if row['open'] - row['close'] > percentile_dic['candle_body_66']:  # 00 - медвежья свеча с телом больших размеров
                code_str += '00'
            elif row['open'] - row['close'] > percentile_dic['candle_body_33']:  # 01 - медвежья свеча с телом средних размеров
                code_str += '01'
            elif row['open'] - row['close'] > 0:  # 10 - медвежья свеча с телом небольших размеров
                code_str += '10'
            # Для верхней тени медвежьей свечи
            if row['high'] - row['open'] > percentile_dic['shadow_high_66']:  # 11 - верхняя тень больших размеров
                code_str += '11'
            elif row['high'] - row['open'] > percentile_dic['shadow_high_33']:  # 10 - верхняя тень средних размеров
                code_str += '10'
            elif row['high'] - row['open'] > 0:  # 01 - верхняя тень небольших размеров
                code_str += '01'
            else:  # 00 - верхняя тень отсутствует
                code_str += '00'
            # Для нижней тени медвежьей свечи
            if row['close'] - row['low'] > percentile_dic['shadow_low_66']:  # 00 - нижняя тень больших размеров
                code_str += '00'
            elif row['close'] - row['low'] > percentile_dic['shadow_low_33']:  # 01 - нижняя тень средних размеров
                code_str += '01'
            elif row['close'] - row['low'] > 0:  # 10 - нижняя тень небольших размеров
                code_str += '10'
            else:  # 11 - нижняя тень отсутствует
                code_str += '11'

        # Свеча на повышение (бычья)
        elif row['open'] < row['close']:  # Свеча на повышение (бычья)
            code_str += '1'
            # Для тела бычьей свечи
            if row['close'] - row['open'] > percentile_dic['candle_body_66']:  # 11 - бычья свеча с телом больших размеров.
                code_str += '11'
            elif row['close'] - row['open'] > percentile_dic['candle_body_33']:  # 10 - бычья свеча с телом средних размеров
                code_str += '10'
            elif row['close'] - row['open'] > 0:  # 01 - бычья свеча с телом небольших размеров
                code_str += '01'
            # Для верхней тени бычьей свечи
            if row['high'] - row['close'] > percentile_dic['shadow_high_66']:  # 11 - верхняя тень больших размеров
                code_str += '11'
            elif row['high'] - row['close'] > percentile_dic['shadow_high_33']:  # 10 - верхняя тень средних размеров
                code_str += '10'
            elif row['high'] - row['close'] > 0:  # 01 - верхняя тень небольших размеров
                code_str += '01'
            else:  # 00 - верхняя тень отсутствует
                code_str += '00'
            # Для нижней тени бычьей свечи
            if row['open'] - row['low'] > percentile_dic['shadow_low_66']:  # 00 - нижняя тень больших размеров
                code_str += '00'
            elif row['open'] - row['low'] > percentile_dic['shadow_low_33']:  # 01 - нижняя тень средних размеров
                code_str += '01'
            elif row['open'] - row['low'] > 0:  # 10 - нижняя тень небольших размеров
                code_str += '10'
            else:  # 11 - нижняя тень отсутствует
                code_str += '11'

        # Дожи
        else:  # Дожи
            if row['high'] - row['open'] > row['open'] - row['low']:  # Верхняя тень больше, медвежий дожи
                code_str += '011'
            else:  # Верхняя тень меньше, бычий дожи
                code_str += '100'
                # Для верхней тени дожи
            if row['high'] - row['close'] > percentile_dic['shadow_high_66']:  # 11 - верхняя тень больших размеров
                code_str += '11'
            elif row['high'] - row['close'] > percentile_dic['shadow_high_33']:  # 10 - верхняя тень средних размеров
                code_str += '10'
            elif row['high'] - row['close'] > 0:  # 01 - верхняя тень небольших размеров
                code_str += '01'
            else:  # 00 - верхняя тень отсутствует
                code_str += '00'
            # Для нижней тени дожи
            if row['open'] - row['low'] > percentile_dic['shadow_low_66']:  # 00 - нижняя тень больших размеров
                code_str += '00'
            elif row['open'] - row['low'] > percentile_dic['shadow_low_33']:  # 01 - нижняя тень средних размеров
                code_str += '01'
            elif row['open'] - row['low'] > 0:  # 10 - нижняя тень небольших размеров
                code_str += '10'
            else:  # 11 - нижняя тень отсутствует
                code_str += '11'

        df_candle_code.loc[[index], ['candle_code']] = int(code_str, 2)
        print(int(code_str, 2))

        # break

    print(df_candle_code)
