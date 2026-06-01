import statistics

def calculate_statistics(splitdata):

    stats = []  # Массив хранения информации сегментов

    for segment in splitdata:
        segmentstat = []   # Строка, куда записываем информацию о сегмента

        values = []        # Получаем значения в сегменте для нахождения моды и медианы
        for i in segment:
            values.append(float(i[1]))

        segmentstat.append(len(segment))                # Количество объектов сегмента
        segmentstat.append(statistics.mean(values))     # Среднее значение сегмента
        segmentstat.append(statistics.mode(values))     # Мода сегмента
        segmentstat.append(statistics.median(values))   # Медиана сегмента
        segmentstat.append(float(segment[0][0]))        # Начало сегмента
        segmentstat.append(float(segment[-1][0]))       # Конец сегмента

        # Добавляем информацию о текущем сегменте в общий массив
        stats.append(segmentstat)

    return stats