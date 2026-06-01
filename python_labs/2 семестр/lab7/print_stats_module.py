def print_stats(stats, n):
    # Если пользователь хочет вывести все сегменты
    if n == -1:
        for i in range(len(stats)):
            print(f"Сегмент {i+1}:\n{stats[i]}")
    # Если пользователь хочет вывести определенный сегмент
    else:
        print(f"\n{stats[n]}")