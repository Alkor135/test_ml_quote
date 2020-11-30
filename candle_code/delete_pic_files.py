# -*- coding: utf-8 -*-
"""
Удаляет выбранные по маске файлы
"""
# -*- coding: utf-8 -*-

from pathlib import Path


def del_file(files_lst):
    """
    Функция удаляет файлы с размером 0
    :param path_dir: Получает в аргументе путь до папки
    :return:
    """
    count_del = 0
    count_file = len(files_lst)
    for file in reversed(files_lst):  # Итерируемся по списку в обратном порядке
        file.unlink()  # Удаляем файл
        count_del += 1
    print(f'Из {count_file} файлов, удалено {count_del} файлов')


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
    print(f'Папка {path_dir} содержит {count_file} файлов общим объемом {total_file_size//1000000}MB')


if __name__ == "__main__":
    path_dir = Path('c:/data_prepare_quote_csv/pic/')  # Путь до каталога в котором нужно удалить файлы
    file_mask = '*2020-01.png'  # Маска файлов для удаления
    files_lst = list(path_dir.glob(file_mask))  # Список файлов для удаления
    # print(files_lst)

    del_file(files_lst)
    get_size_dir(path_dir)

