import csv

def read_data_from_file(file):

    lines = []  # Массив для хранения элементов из файла

    # with open(sys.argv[1]) as csvfile:
    with open(file) as csvfile:

        # Создаем массив строк из файла
        file = csv.reader(csvfile, delimiter="\n")

        # Разбиваем строки на элементы
        try:
            for i in file:
                lines.append(i[0].replace("(", "").replace(")", "").split(","))
        except:
            lines = []

    return lines