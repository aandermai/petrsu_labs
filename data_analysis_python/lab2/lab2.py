from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re

line_pattern = re.compile(r"(^15:\d{2}:\d{2}).*\bA00000000002 <--->.*\bKEEP.*\bvolume=(\d+)")
volume_list = []
time_list = []

# Поиск строк, соответствующих шаблону
with open("./n_log2.txt") as file:
    for line in file:
        line_match = line_pattern.search(line)
        if line_match:
            time_list.append(datetime.strptime(line_match.group(1), "%H:%M:%S"))
            volume_list.append(int(line_match.group(2)))

start_time = datetime.strptime("15:00:00", "%H:%M:%S")
end_time = datetime.strptime("16:00:00", "%H:%M:%S")
step = timedelta(minutes=10)

# Интервал первые 10 минут
ten_mins_interval = []
ten_mins_volume = []

for time, volume in zip(time_list, volume_list):
    if start_time <= time < start_time + step:
        ten_mins_interval.append(time)
        ten_mins_volume.append(volume)

# Интервал часа по 10 минут
one_hour_interval = []
one_hour_volume = []

for i in range(6):
    interval_start = start_time + i * step
    interval_end = interval_start + step

    volumes = []

    for time, volume in zip(time_list, volume_list):
        if interval_start <= time < interval_end:
            volumes.append(volume)

    average_volume = sum(volumes) / len(volumes)

    one_hour_interval.append(i)
    one_hour_volume.append(average_volume)

fig = plt.figure(figsize=(12,5))
plt.subplots_adjust(hspace=0.5)

# Первый график
ax1 = fig.add_subplot(2, 1, 1)
ax1.plot(ten_mins_interval, ten_mins_volume, label="A00000000002")
ax1.set_title("График1. Volume")
ax1.set_xlabel("Время")
ax1.set_ylabel("Volume")
ax1.legend()
ax1.xaxis.set_major_locator(mdates.MinuteLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

# Второй график
ax2 = fig.add_subplot(2, 1, 2)
ax2.plot(one_hour_interval, one_hour_volume, label="A00000000002")
ax2.set_title("График2. Volume по 10-мин")
ax2.set_xlabel("Номер 10-минутки")
ax2.set_ylabel("Volume")
ax2.legend()

plt.show()