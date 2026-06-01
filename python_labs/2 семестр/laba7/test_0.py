import os
import read_data_from_file_module
import split_data_module
import calculate_statistics_module

file = 'ccsv.csv'

time = 300

# нет указанного файла asda
def test_file_exist():
    assert os.path.exists(file), f"Файл {file} не существует."


# файл не имеет прав на чтение asda
def test_file_read():
    assert os.access(file, os.R_OK), f"Нет прав на чтение файла {file}."


# файл не формата csv и не txt asda
def test_file_csv():
    assert (file.split('.')[1] == "csv" or file.split('.')[1] == "txt"), f"Файл {file} имеет недопустимое расширение."


# 1/3 - проверка на пустой файл aaa
def test_empty_file():
    lines = read_data_from_file_module.read_data_from_file(file)
    assert len(lines) > 0, f"Файл пустой"


# в какой-то из строк файла не два элемента bbb
def test_data_split():
    lines = read_data_from_file_module.read_data_from_file(file)

    for i in range(len(lines)):
        assert len(lines[i]) == 2, f"{i+1} строка не содержит два элемента."


# данные не заданного типа
def test_flow_int():
    lines = read_data_from_file_module.read_data_from_file(file)

    for i in range(len(lines)):
        assert (lines[i][0].replace(".", "").replace("-", "").isdigit() and lines[i][1].isdigit()), f"{i+1} строка не содержит заданный тип."


# 2/3 - есть ли отрицательные временные значения bbb
def test_minus_time():
    lines = read_data_from_file_module.read_data_from_file(file)
    print(lines[0][0])
    for i in range(len(lines)):
        assert float(lines[i][0]) >= 0, f"В {i+1} строке отрицательное время."


# файл делится на нужные интервалы по времени ссс???
def test_intervals():
    lines = read_data_from_file_module.read_data_from_file(file)
    segments = split_data_module.split_data(lines, time)
    for i in range(len(segments)):
        assert float(segments[i][-1][0]) - float(segments[i][0][0]) < time, f"Интервал в строке {i+1} не соответствует ожидаемому."
        # assert float(segments[i][-1][0]) - float(segments[i][0][0]) + 1000 < time, f"Интервал в сегменте {i+1} не соответствует ожидаемому."



# правильное количество интервалов ccc
def test_intervals_count():
    lines = read_data_from_file_module.read_data_from_file(file)
    segments = split_data_module.split_data(lines, time)
    assert len(segments) == 44, f"Количество интервалов не соответствует ожидаемому."


# статистики подсчитываются верно ccc
def test_statistics_intervals():
    lines = read_data_from_file_module.read_data_from_file(file)
    segments = split_data_module.split_data(lines, time)
    statistics = calculate_statistics_module.calculate_statistics(segments)

    if len(segments) == 1:
        kik = 0
    else:
        kik = 1

    for i in range(len(segments)-kik):
        assert (300 <= statistics[i][0] <= 400), f"Количество объектов сегмента {i+1} не соответствует ожидаемому."
        assert (150 <= statistics[i][1] <= 270), f"Среднее значение сегмента {i+1} не соответствует ожидаемому."
        assert (150 <= statistics[i][2] <= 270), f"Мода сегмента {i+1} не соответствует ожидаемому."
        assert (150 <= statistics[i][3] <= 270), f"Медиана сегмента {i+1} не соответствует ожидаемому."


# Есть ли временные значения меньше, чем предыдущие bbb
def test_right_time():
    lines = read_data_from_file_module.read_data_from_file(file)
    for i in range(1, len(lines)):
        assert float(lines[i-1][0]) <= float(lines[i][0]), f"Предыдущее время больше, чем в {i+1} строке."
