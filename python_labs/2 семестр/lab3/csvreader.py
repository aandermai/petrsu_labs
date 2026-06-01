import csv
import statistics
import sys
import split_data as split_data


# считывание данных из файла
def read_data_from_file():

    lines = []  # Массив для хранения элементов из файла

    with open(sys.argv[1]) as csvfile:
        # with open('ccsv.csv') as csvfile:

        # Создаем массив строк из файла по разделителю '\n'
        file = csv.reader(csvfile, delimiter="\n")

        # Разбиваем строки на элементы
        for i in file:
            lines.append(i[0].split(","))

    return lines


# вычисление статистики для сегментов
def calculate_statistics(splitdata):

    stats = []  # Массив хранения информации сегментов

    for segment in splitdata:
        segmentstat = ""  # Строка, куда записываем информацию о сегмента

        values = []  # Получаем значения в сегменте для нахождения моды и медианы
        for i in segment:
            values.append(float(i[1]))

        segmentstat += f"Количество объектов: {len(segment)}\n"
        segmentstat += f"Среднее значение: {statistics.mean(values)}\n"
        # значение, которое встречается наиболее часто в наборе данных
        segmentstat += "Мода: " + f"{statistics.multimode(values)}"[1:-1] + "\n"
        # центральное значение набора данных
        segmentstat += f"Медиана: {statistics.median(values)}\n"
        segmentstat += f"Начало: {float(segment[0][0])}\n"
        segmentstat += f"Конец: {float(segment[-1][0])}\n"

        # Добавляем информацию о текущем сегменте в общий массив
        stats.append(segmentstat)

    return stats


# вывод статистики
def print_stats(stats, n):
    # Если пользователь хочет вывести все сегменты
    if n == -1:
        for i in range(len(stats)):
            print(f"Сегмент {i+1}:\n{stats[i]}")
    # Если пользователь хочет вывести определенный сегмент
    else:
        print(f"\n{stats[n]}")


lines = read_data_from_file()
splitdata = split_data.split_data(lines)
stats = calculate_statistics(splitdata)
n = int(input("Какой сегмент вывести?\nЕсли хотите вывести все, то напишите 0\n")) - 1
print_stats(stats, n)
