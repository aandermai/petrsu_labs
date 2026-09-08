from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import re

line_pattern = re.compile(r".*\bA00000000002 <--->.*?\bKEEP")
volume_pattern = re.compile(r"\bvolume=(\d+)")
time_pattern = re.compile(r"(^15:\d{2}:\d{2})")

volume_list = []
time_list = []

# Поиск строк, соответствующих шаблону
with open("n_log2.txt") as file:
    for line in file:
        if line_pattern.search(line):
            time_match = time_pattern.search(line)
            volume_match = volume_pattern.search(line)
            
            if time_match and volume_match:
                time_list.append(time_match.group(1))
                volume_list.append(int(volume_match.group(1)))

# Преобразование времени в объекты datetime
time_datetime = [datetime.strptime(t, "%H:%M:%S") for t in time_list]
start_time = datetime.strptime("15:00:00", "%H:%M:%S")
end_time = datetime.strptime("16:00:00", "%H:%M:%S")
step = timedelta(minutes=10)

# 1) Данные за первый 10-минутный интервал
first_interval_end = start_time + step
first_interval_data = {}
for t, v in zip(time_datetime, volume_list):
    if start_time <= t < first_interval_end:
        first_interval_data[t.strftime("%H:%M:%S")] = v

# 2) Разбиение на 10-минутные интервалы и вычисление средних
intervals = []
interval_means = []
current = start_time

while current < end_time:
    next_time = current + step
    interval_volumes = []
    
    for t, v in zip(time_datetime, volume_list):
        if current <= t < next_time:
            interval_volumes.append(v)
    
    if interval_volumes:  # если есть данные в интервале
        intervals.append(f"{current.strftime('%H:%M')}-{next_time.strftime('%H:%M')}")
        interval_means.append(sum(interval_volumes) / len(interval_volumes))
    
    current = next_time

# Создание графиков
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Первый график - данные за первый 10-минутный интервал
ax1.plot(list(first_interval_data.keys()), list(first_interval_data.values()), label='A00000000002')
ax1.set_xlabel('Время')
ax1.set_ylabel('Volume')
ax1.legend()
ax1.tick_params(axis='x', rotation=45)

# Второй график - средние значения по 10-минутным интервалам
ax2.plot(range(1, len(interval_means) + 1), interval_means, 
         'ro-', label='A00000000002')
ax2.set_xlabel('Номер временного отрезка (10 минут)')
ax2.set_ylabel('Среднее значение volume')
ax2.set_title('Средние значения volume по 10-минутным интервалам')
ax2.legend()
ax2.set_xticks(range(1, len(interval_means) + 1))

plt.tight_layout()
plt.show()

