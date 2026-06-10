current_position = [1, 1]  # текущая позиция
main_positions = []  # список с главными позициями
all_positions = []  # список со всеми позициями
step = []  # список с командами


def valid_position(position):  # проверяем, находится ли робот в пределах поля
    return 1 <= position[0] < 100 and 1 <= position[1] < 100


while True:
    step = input("Введите команду: ")

    if step == "B":
        step = "B,1"

    step = step.split(",")

    if not (step[0] in ["R", "L", "D", "U", "B"] and int(step[1].isdigit())):  # проверяем, правильно ли пользователь ввел данные
        print("Данные введены неверно")
        break

    main_positions.append(current_position.copy())

    for i in range(int(step[1])):

        if not (valid_position(current_position)):
            print("Робот вышел за пределы поля")
            quit()

        # узнаем направление робота и перемещаем его
        if step[0] == "L":
            current_position[0] -= 1

        elif step[0] == "R":
            current_position[0] += 1

        elif step[0] == "U":
            current_position[1] -= 1

        elif step[0] == "D":
            current_position[1] += 1

        elif step[0] == "B":

            if int(step[1]) > len(main_positions):
                all_positions, main_positions, current_position = [], [], [1, 1]
                print(
                    "Количество команд недостаточно\nРобот вернулся на исходную позицию"
                )
                print(*current_position, sep=",")
                break

            else:
                while all_positions[-1] != main_positions[-1]:
                    print(*all_positions[-1], sep=",")
                    all_positions.pop()
                main_positions.pop()
                current_position = main_positions[-1]

        print(*current_position, sep=",")
        all_positions.append(current_position.copy())
