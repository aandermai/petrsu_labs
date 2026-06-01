def split_data(lines, time):
    splitdata = []  # Массив с раделенными на время элементами
    n = time
    k = 0
    j = -1
    for i in lines:
        # Если время строки меньше k, то записываем его во фрагмент j
        if float(i[0]) <= k:
            splitdata[j].append(i)
        # Иначе создаем новый фрагмент j и записываем строку в него
        else:
            splitdata.append([])
            k += n
            j += 1
            splitdata[j].append(i)

    return splitdata
