import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def convert_data_to_array(column_name: str) -> list[float]:
    '''
    Перевод формата Excel-таблиц в массив.

    Аргументы:
    - column_name - имя столбца, с которого берутся данные
    '''
    df = pd.read_excel("./statistic_table_lab1.xlsx", usecols=[f"{column_name}"])
    return df[column_name].tolist()

def calculate_metrics(data: list[float]) -> None:
    '''
    Высчитывание метрик для выборки: математическое ожидание, дисперсия, отклонение,
    начальные и центральные моменты до 4 порядка, ассиметрия, медиана, эксцесс.

    Аргументы:
    - data - выборка в формате массива
    '''
    # Переводим наши данные в numpy-массив, чтобы всё работало побыстрее
    data = np.array(data)

    # Математическое ожидание
    mean = np.mean(data)

    """
    Дисперсия и среднеквадратичное отклонение.

    Про ddof=1: мы используем этот параметр, потому что у нас не генеральная совокупность, т.е. у нас не прям все данные, так как некоторые регионы выкинуты.
    Единственное отличие от формулы будет, что вместо того, чтобы делить на n, мы делим на n+1.
    """
    varience = np.var(data, ddof=1) 
    std_dev = np.std(data, ddof=1)

    # Начальные моменты с 1 по 4 порядок
    start_momement_1 = mean 
    start_momement_2 = np.mean(data**2)
    start_momement_3 = np.mean(data**3)
    start_momement_4 = np.mean(data**4)
    # Центральные моменты с 1 по 4 порядок
    central_moment_1 = np.mean(data - mean)
    central_moment_2 = np.mean((data - mean)**2)
    central_moment_3 = np.mean((data - mean)**3)
    central_moment_4 = np.mean((data - mean)**4)
    # Ассиметрия
    skewness = central_moment_3 / (std_dev**3) 
    # Медиана
    median = np.median(data) 
    # Эксцесс
    kurtosis = central_moment_4 / (std_dev**4) 

    print(f"Математическое ожидание: {mean}")
    print(f"Дисперсия: {varience}")
    print(f"Среднеквадратическое отклонение: {std_dev}")
    print(f"Начальный момент 1-ого порядка: {start_momement_1}")
    print(f"Начальный момент 2-ого порядка: {start_momement_2}")
    print(f"Начальный момент 3-ого порядка: {start_momement_3}")
    print(f"Начальный момент 4-ого порядка: {start_momement_4}")
    print(f"Центральный момент 1-ого порядка: {central_moment_1}")
    print(f"Центральный момент 2-ого порядка: {central_moment_2}")
    print(f"Центральный момент 3-ого порядка: {central_moment_3}")
    print(f"Центральный момент 4-ого порядка: {central_moment_4}")
    print(f"Коэффицент ассиметрии: {skewness}")
    print(f"Медиана: {median}")
    print(f"Эксцесс: {kurtosis}")

def create_hist(data: list[float], title: str) -> None:
    '''
    Построение гистограммы, полигона частот и эмпирической функции для выборки.

    Аргументы:
    - data - выборка в формате массива;
    - title - заголовок столбца выборки
    '''
    fig, axes = plt.subplots(1, 3, figsize=(10, 5))
    fig.suptitle(title, fontsize=16)

    # Гистограмма
    counts, bins, _ = axes[0].hist(data, bins=10, edgecolor="black")
    axes[0].set_title("Гистограмма")
    axes[0].set_xlabel("Значение")
    axes[0].set_ylabel("Частота")

    # Полигон частот
    centers = (bins[:-1] + bins[1:]) / 2
    axes[1].plot(centers, counts, marker='o')
    axes[1].set_title("Полигон частот")
    axes[1].set_xlabel("Интервалы")
    axes[1].set_ylabel("Частота")

    # Эмпирическая функция
    sorted_data = np.sort(data)
    n = len(data)
    y = np.arange(1, n + 1) / n

    axes[2].step(sorted_data, y, where="post")
    axes[2].set_title("Эмпирическая функция")
    axes[2].set_xlabel("x")
    axes[2].set_ylabel("F(x)")

    plt.tight_layout()
    plt.show()

def confidence_interval_mean(data: list[float], p: float) -> None:
    '''
    Расчёт доверительных интервалов для математического ожидания выборки.

    Аргументы:
    - data - выборка в формате массива;
    - p - доверительная вероятность
    '''
    data = np.array(data) # Выборка
    n = len(data) # Количество элементов выборки
    mean = np.mean(data) # Математическое ожидание
    std = np.std(data, ddof=1) # Среднеквадратичное отклонение 
    alpha = 1 - p # Уровень значимости    

    # Находим критическое значение Z из нормального распределения
    z_value = stats.norm.ppf(1 - alpha/2)

    # Считаем погрешность (ширину интервала). std / sqrt(n) — стандартная ошибка среднего
    margin = z_value * std / np.sqrt(n)

    # Левая и правая границы доверительного интервала
    left = mean - margin 
    right = mean + margin

    print(f"\nДоверительный интервал для p={p}:")
    print(f"[{left}, {right}]")

data1 = convert_data_to_array("Уровень инновационного производства")
calculate_metrics(data1)
confidence_interval_mean(data1, 0.95)
confidence_interval_mean(data1, 0.99)
create_hist(data1, "Уровень инновационного производства")
print()

data2 = convert_data_to_array("Количество студентов (СПО)")
calculate_metrics(data2)
confidence_interval_mean(data2, 0.95)
confidence_interval_mean(data2, 0.99)
create_hist(data2, "Количество студентов (СПО)")
print()

data3 = convert_data_to_array("Количество студентов (ВПО)")
calculate_metrics(data3)
confidence_interval_mean(data3, 0.95)
confidence_interval_mean(data3, 0.99)
create_hist(data3, "Количество студентов (ВПО)")
print()

data4 = convert_data_to_array("ВРП")
calculate_metrics(data4)
confidence_interval_mean(data4, 0.95)
confidence_interval_mean(data4, 0.99)
create_hist(data4, "ВРП")
print()

data5 = convert_data_to_array("Розничные продажи")
calculate_metrics(data5)
confidence_interval_mean(data5, 0.95)
confidence_interval_mean(data5, 0.99)
create_hist(data5, "Розничные продажи")
print()

data6 = convert_data_to_array("Потребительские расходы")
calculate_metrics(data6)
confidence_interval_mean(data6, 0.95)
confidence_interval_mean(data6, 0.99)
create_hist(data6, "Потребительские расходы")