import sys
import os
import filecmp  # для сравнения файлов


def gealfiles():
    # Считываем имя католога, в котором будет осуществляться поиск
    startdir = sys.argv[1]
    filearray = []

    # Проходим по всем поддиректориям и файлам в начальной директории
    for subdir, dirs, files in os.walk(startdir):
        # Перебираем файлы в директории
        for file in files:
            # Добавляем полный путь к файлу в список файлов
            filearray.append(os.path.join(subdir, file))

    return filearray


def getsamesfiles(filearray):
    samefilesarray = []

    for i in range(len(filearray)):
        samefiles = [filearray[i]]
        for j in range(i + 1, len(filearray)):
            # Сравнение файлов по содержимому и занесение их в массив
            if filecmp.cmp(filearray[i], filearray[j], shallow=False):
                samefiles.append(filearray[j])

        # Проверяем, есть ли массив с подобными копиями. Если нет, то добавляем
        if len(samefiles) > 1:
            flag = 0
            for k in range(len(samefilesarray)):
                if any(elem in samefilesarray[k] for elem in samefiles):
                    flag += 1
            if flag == 0:
                samefilesarray.append(samefiles)

    if len(samefilesarray) == 0:
        print("\nНе было найдено одинаковых файлов\n")
        exit()
    return samefilesarray


def delsamesfiles(samefilesss):
    for samefiles in samefilesss:
        print("\nНайденные одинаковые файлы:\n")
        # Вывод одинаковых файлов для последующего пользовательского удаления
        for i in range(len(samefiles)):
            print(f"{str(i+1)}) {samefiles[i]}")
        print("\nВведите номер файла, который хотите сохранить.\n")

        while True:
            usrinput = input("Ввод: ")
            if usrinput == "n":
                break

            # Проверка на правильный ввод команды
            try:
                dupeind = int(usrinput) - 1
            except:
                print("\nНеверно введена команда.\n")
                continue

            # Удаление файлов, что не стоят по выбранному итератору в массиве
            if 0 <= dupeind <= len(samefiles):
                for i in range(len(samefiles)):
                    if i != dupeind:
                        os.remove(samefiles[i])
                break
            else:
                print("\nНеправильный ввод номера файла.\n")


delsamesfiles(getsamesfiles(gealfiles()))
input("\nЗавершение программы.")
