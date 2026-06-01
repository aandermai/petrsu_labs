import sys

# проверка на ввод файла в командной строке
if len(sys.argv) != 2:
    print("Введено неверное количество аргументов")
    sys.exit(1)

# принимаем в командной строке имя файла, в котором будем выполнять команды
textfile = sys.argv[1]

history = []  # список выполненных команд
copy_list = [] # список для команды copy
command_tuple = (
    "insert",
    "save",
    "undo",
    "swap",
    "delcol",
    "delrow",
    "exit",
    "show",
    "del",
    "copy",
    "paste"
)  # наши команды

with open(textfile, encoding="utf-8") as file:
    lines = file.readlines()

# команда insert (вставить текст)
def insert(text, num_row=None, num_col=None):
    if num_row is None:  # не указана строка
        lines.append(text + "\n")
    else:
        num_row -= 1
        if num_col is None:  # не указан столбец
            lines.insert(num_row, text + "\n")
        else:
            line = lines[num_row]
            lines[num_row] = line[: num_col - 1] + text + " " + line[num_col - 1 :]

# команда undo (отмена команды)
def undo(num_operations=1):
    lines[:] = history[-1]
    for i in range(num_operations):
        history.pop()

# команда delcol (удалить столбец)
def del_column(col_number):
    for i in range(len(lines)):
        columns = lines[i].split()  # разбиваем строку на отдельные столбцы
        if len(columns) >= col_number:
            del columns[col_number - 1]  # удаляем указанный столбец
            lines[i] = " ".join(columns) + "\n"  # обновляем строку

# команда swap (поменять строки местами)
def swap_rows(row1, row2):
    if not lines[-1].endswith("\n"):  # добавляем пустую строку, чтобы ничего не съехало
        lines[-1] += "\n"

    if 1 <= row1 <= len(lines) and 1 <= row2 <= len(lines):
        lines[row1 - 1], lines[row2 - 1] = lines[row2 - 1], lines[row1 - 1]

    if lines:  # удаляем добавленную пустую строку, чтобы всё было, как до этого
        lines[-1] = lines[-1].rstrip("\n")

# команда delrow (удалить строку)
def delete_row(num_row):
    if num_row <= len(lines):
        del lines[num_row - 1]
    else:
        print("Ошибка: недостаточно строк в файле")

# команда show (показать содержимое файла)
def show_content():
    for line in lines:
        line = line.rstrip("\n")
        print(line)

# команда del (удалить содержимое файла)
def delete_content():
    lines.clear()
    print("Содержимое файла удалено")

# команда save (сохранить файл)
def save_file():
    with open(textfile, "w", encoding="utf-8") as file:
        file.writelines(lines)

while True:
    command = input("Введите команду: ")

    if not command.startswith(command_tuple):
        print("Неправильно введена команда")

    if command == "show":
        show_content()

    elif command.startswith("insert"):
        history.append(lines[:])
        parts = command.split()
        if len(parts) < 2:
            print("Ошибка: не указан текст для вставки")
        else:
            text = parts[1].strip('"')
            num_row = int(parts[2]) if len(parts) > 2 else None
            num_col = int(parts[3]) if len(parts) > 3 else None
            insert(text, num_row, num_col)

    elif command.startswith("undo"):
        parts = command.split()
        num_operations = int(parts[1]) if len(parts) > 1 else 1
        if num_operations >= len(history):
            undo(len(history) - 1)
            print("Файл вернулся к исходному")
        else:
            undo(num_operations)

    elif command.startswith("delrow"):
        history.append(lines[:])
        parts = command.split()
        if len(parts) < 2:
            print("Не указан номер строки.")
            continue
        row_number = int(parts[1])
        delete_row(row_number)

    elif command.startswith("swap"):
        history.append(lines[:])
        parts = command.split()
        if len(parts) < 3:
            print("Не указаны номера строк для обмена.")
            continue
        row1 = int(parts[1])
        row2 = int(parts[2])
        swap_rows(row1, row2)

    elif command.startswith("delcol"):
        history.append(lines[:])
        parts = command.split()
        if len(parts) < 1:
            print("Не указан номер столбца.")
            continue
        col_number = int(parts[1])
        del_column(col_number)

    elif command.startswith("copy"):
        parts = command.split()
        if len(parts) != 2:
            print("Ошибка. Не введён номер строки")
            continue
        num_row = int(parts[1])
        copy_list.append(lines[num_row - 1])

    elif command.startswith("paste"):
        history.append(lines[:])
        parts = command.split()
        if len(parts) != 2:
            print("Ошибка. Не введён номер строки")
        num_row = int(parts[1])
        lines.pop(num_row - 1)
        lines.insert(num_row - 1, copy_list[0])

    elif command == "save": 
        save_file()

    elif command == "del":
        history.append(lines[:])
        delete_content()

    # команда exit (выход из редактора)
    elif command == "exit":
        break
