# -*- coding: utf-8 -*-
"""
Закачивает исторические данные с ФИНАМа, за указанный период, в указанном формате
Каждый день в своем файле
Настройки внизу.
"""
from urllib.parse import urlencode
from urllib.request import urlopen
from datetime import datetime
from pathlib import Path
from settings import *
import pandas as pd
import time


class DownloadFinam:
    def __init__(self, ticker, path_data, period=3, market=14):
        self.path_data = path_data
        self.ticker = ticker
        self.period = period
        self.market = market
        self.datf = 9  # Для тиков
        self.url = ''

    def create_url_finam(self, download_date):
        """
        Функция составляет url для запроса на сервер FINAMa
        :param download_date: Получает в аргументе дату за которую нужно скачать котировки (один день)
        :return: Переопределяет self.url
        """
        if self.period == 1:  # Если период выбран тики
            self.datf = 9  # Формат записи для тиков
        else:
            self.datf = 5  # Формат записи для минутных баров 'DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL'

        start_date = datetime.strptime(download_date, "%Y%m%d").date()  # Переводим формат в datetime
        end_date = start_date

        # Все параметры упаковываем в единую структуру.
        # Здесь есть дополнительные параметры, кроме тех, которые заданы в шапке. См. комментарии.
        params = urlencode([
            ('market', self.market),  # на каком рынке торгуется бумага
            ('em', TICKERS[ticker]),  # вытягиваем цифровой символ, который соответствует бумаге.
            ('code', self.ticker),  # тикер фин инструмента
            ('apply', 0),  # не нашёл что это значит.
            ('df', start_date.day),  # Начальная дата, номер дня (1-31)
            ('mf', start_date.month - 1),  # Начальная дата, номер месяца (0-11)
            ('yf', start_date.year),  # Начальная дата, год
            ('from', start_date),  # Начальная дата полностью
            ('dt', end_date.day),  # Конечная дата, номер дня
            ('mt', end_date.month - 1),  # Конечная дата, номер месяца
            ('yt', end_date.year),  # Конечная дата, год
            ('to', end_date),  # Конечная дата
            ('p', self.period),  # Таймфрейм
            ('f', self.ticker + "_" + download_date),  # Имя сформированного файла
            ('e', ".csv"),  # Расширение сформированного файла
            ('cn', self.ticker),  # ещё раз тикер
            # См.страницу  # https://www.finam.ru/profile/moex-akcii/sberbank/export/
            ('dtf', 1),  # В каком формате брать даты. Выбор из 5 возможных.
            ('tmf', 1),  # В каком формате брать время. Выбор из 4 возможных.
            ('MSOR', 0),  # Время свечи (0 - open; 1 - close)
            ('mstime', "on"),  # Московское время
            ('mstimever', 1),  # Коррекция часового пояса
            ('sep', 1),  # Разделитель полей	(1 - запятая, 2 - точка, 3 - точка с запятой, 4 - табуляция, 5 - пробел)
            ('sep2', 1),  # Разделитель разрядов
            ('datf', self.datf),  # Формат записи в файл. Выбор из 11 возможных (1-для минутных баров, 7-для тиков).
            ('at', 1)  # Нужны ли заголовки столбцов
        ])

        self.url = f'{FINAM_URL}{ticker}_{download_date}_{download_date}.csv?{params}'  # урл составлен!
        print(f'Ссылка для запроса готова: {self.url}')

    def path_file(self, file_name_date):
        """
        Функция создает имя файла и путь его сохранения
        :param file_name_date: Получает в аргументе дату которую добавляет к имени файла
        :return: Возвращает путь и имя для сохранения файла
        """
        period_txt = PERIODS[period]  # Для добавления к имени файла периода
        file_name = f'{self.ticker}_{period_txt}_{file_name_date}.csv'  # Имя выходного файла

        dir_path = Path(self.path_data)  # Папка для сохранения (родительский каталог, папка data)
        if not dir_path.exists():  # Проверяем существует ли папка
            dir_path.mkdir()  # Создаем папку при её отсутствии

        return Path(f'{self.path_data}/{file_name}')  # Создаем пути для сохранения файла

    def run(self, download_date, file_name_date):
        """

        :param download_date: Дата за которую нужно скачать котировки
        :param file_name_date: Дата для подстановки в имя файла
        :return:
        """
        self.create_url_finam(download_date)  # Вызываем функцию составления url
        file_path = self.path_file(file_name_date)  # Вызываем функцию составления путей и имени файла
        if not file_path.exists():  # Если файла не существует
            txt = urlopen(self.url).readlines()  # Получаем в txt массив данных с Финама.

            with open(file_path, 'w', encoding='utf-8') as file_out:  # задаём файл, в который запишем котировки.
                for line in txt:  # записываем файл строку за строкой.
                    file_out.write(line.strip().decode("utf-8") + '\n')

            print(f'Готово. Проверьте файл {file_path} по указанному пути')
            time.sleep(2)  # Сон в 2 секунды (для того, чтобы не перегружать сервер ФИНАМа)
        else:
            print(f'Файл {file_path} уже существует')


if __name__ == "__main__":

    """ 
    Основные настройки параметров загрузки котировок.
    Проверьте наличие тикера в файле settings.py
    """
    path_data = 'c:/data_finam_quote_csv'  # Папка для сохранения файлов котировок (папка c:/data_finam_csv)
    ticker = "SPFB.RTS"  # задаём тикер
    period = 1  # задаём период. Выбор из: 'tick': 1, 'min': 2, '5min': 3, '10min': 4, '15min': 5, '30min': 6, 'hour': 7
    start = "01.01.2019"  # с какой даты начинать тянуть котировки
    end = "01.01.2020"  # финальная дата, по которую тянуть котировки
    market = 14  # FUTURES = 14  non-expired futures; АКЦИИ = 0

    # Далее идет исполняемый код (не настройки)
    # Делаем преобразования дат:
    start_date_range = datetime.strptime(start, '%d.%m.%Y').strftime('%Y%m%d')  # Дата в нужном формате строкой
    end_date_range = datetime.strptime(end, '%d.%m.%Y').strftime('%Y%m%d')
    date_range = pd.date_range(start_date_range, end_date_range)  # Список дат в диапазоне

    data = DownloadFinam(ticker, path_data, period, market)  # Создаем экземпляр класса
    for single_date in date_range:
        download_date = single_date.strftime('%Y%m%d')  # Дата для закачки котировок
        file_name_date = single_date.strftime('%y%m%d')  # Дата которую будем подставлять в имя файла
        data.run(download_date, file_name_date)
    print('Закачка которовок завершена. Удалите пустые файлы.')
