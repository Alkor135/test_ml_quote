# -*- coding: utf-8 -*-
"""
Удаляет файлы нулевой длины.
Выводит информацию о количестве удаленных файлов и об оставшихся файлах.
"""
from pathlib import Path


def del_file(path_dir):
    """
    Функция удаляет файлы с размером 0
    :param path_dir: Получает в аргументе путь до папки
    :return:
    """
    file_lst = list(path_dir.glob('*'))  # Создание списка всех файлов
    count_del = 0
    count_file = 0
    for file in reversed(file_lst):  # Итерируемся по списку в обратном порядке
        if Path(file).stat().st_size == 0:  # Если файл с нулевым размером
            file.unlink()  # Удаляем файл
            count_del += 1
        count_file += 1
    print(f'Из {count_file} файлов, удалено {count_del} пустых файлов')
    # return count_file, count_del


def get_size_dir(path_dir):
    """
    Функция подсчитывает общий объем всех файлов в каталоге и подкаталогах
    :param path_dir: Получает в аргументе путь до папки
    :return:
    """
    file_lst = list(path_dir.glob('**/*'))  # Все файлы во всех подкаталогах
    total_file_size = 0
    count_file = 0
    for file in file_lst:
        total_file_size += Path(file).stat().st_size
        count_file += 1
    print(f'Папка {path_dir} содержит {count_file} файлов общим объемом {total_file_size // 1000000}MB')


if __name__ == "__main__":
    # path_storage = Path('../data_finam')  # Путь до каталога data_finam который находиться в родит. каталоге
    path_storage = Path('c:/data_finam_quote_csv')  # Путь по которому нужно стереть пустые файлы

    del_file(path_storage)
    get_size_dir(path_storage)
