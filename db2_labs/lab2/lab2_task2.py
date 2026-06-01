import customtkinter
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
import redis

# Очистка данных и закрытие приложения
def on_closing():
    if askyesno("Выход", "Закрыть приложение и обнулить все оценки?"):
        # Очищаем все оценки судей
        judges = r.zrange("judges:info", 0, -1)
        for judge in judges:
            judge_key = f"judge:{judge}"
            # Удаляем упорядоченное множество этого судьи
            r.delete(judge_key)
        
        # Обнуляем общие рейтинги спортсменов
        sportsmans = r.zrange("sportsmans:info", 0, -1)
        for sportsman in sportsmans:
            r.zadd("sportsmans:ratings", {sportsman: 0})

        root.destroy()

# Обновление таблицы рейтингов
def update_rating_table():
    # Очищаем таблицу
    for item in rating_table.get_children():
        rating_table.delete(item)
    
    # Получаем всех спортсменов с их рейтингами от большего к меньшему
    sportsmans_with_scores = r.zrevrange("sportsmans:ratings", 0, -1, withscores=True)
    
    # Заполняем таблицу
    for sportsman, score in sportsmans_with_scores:
        rating_table.insert("", END, values=[sportsman, f"{score:.1f}"])


# Добавление очков спортсмену
def save_results():
    judge = judge_combobox.get() # Судья
    sportsman = sportsman_combobox.get() # Спортсмен
    points = float(point_spinbox.get()) # Баллы
    
    # Проверяем, что все поля заполнены
    if judge == "" or sportsman == "":
        showerror("Ошибка", "Выберите судью и спортсмена")
        return
    
    # Ключ для упорядоченного множества этого судьи
    judge_key = f"judge:{judge}"
    
    # Получаем предыдущую оценку этого судьи этому спортсмену (если есть)
    previous_score = r.zscore(judge_key, sportsman)
    previous_score = previous_score if previous_score is not None else 0.0
    
    # Обновляем оценку в упорядоченном множестве судьи
    r.zadd(judge_key, {sportsman: points})
    
    # Вычитаем старую оценку и добавляем новую
    current_total = r.zscore("sportsmans:ratings", sportsman)
    current_total = current_total if current_total is not None else 0.0
    
    new_total = current_total - previous_score + points
    
    # Обновляем упорядоченное множество общих рейтингов
    r.zadd("sportsmans:ratings", {sportsman: new_total})
    
    # Обновляем таблицу
    update_rating_table()
    
    showinfo("Успех", f"Судья {judge} поставил {points} баллов спортсмену {sportsman}")

# Подключение к БД
r = redis.StrictRedis(host="127.0.0.1", port=6379, password="student", decode_responses=True, db=1)
print(f'Результат подключения: {r.ping()}')

# Создание основного окна
root = customtkinter.CTk()
root.geometry("1000x500")
root.title("Спортивное табло")

# Поле выбора судьи
judge_frame = customtkinter.CTkFrame(root, fg_color="transparent")
judge_label = customtkinter.CTkLabel(judge_frame, text="Судья", fg_color="transparent", font=("Steppe", 17))
judge_combobox = customtkinter.CTkComboBox(judge_frame, values=r.zrange("judges:info", 0, -1))
judge_combobox.set("")
judge_frame.pack()
judge_label.pack()
judge_combobox.pack()

# Поле ввода баллов
point_var = StringVar(value=0.0)
point_frame = customtkinter.CTkFrame(root, fg_color="transparent")
point_label = customtkinter.CTkLabel(point_frame, fg_color="transparent", text="Баллы", font=("Steppe", 17))
point_spinbox = ttk.Spinbox(point_frame, textvariable=point_var, from_=0.0, to=10.0, increment=0.1, width=30, wrap=True)
point_frame.pack()
point_label.pack()
point_spinbox.pack()

# Поле выбора спортсмена
sportsman_frame = customtkinter.CTkFrame(root, fg_color="transparent")
sportsman_label = customtkinter.CTkLabel(sportsman_frame, fg_color="transparent", text="Спортсмен", font=("Steppe", 17))
sportsman_combobox = customtkinter.CTkComboBox(sportsman_frame, values=r.zrange("sportsmans:info", 0, -1))
sportsman_combobox.set("")
sportsman_frame.pack(pady=15)
sportsman_label.pack()
sportsman_combobox.pack()

# Кнопка сохранения результатов
save_button = customtkinter.CTkButton(sportsman_frame, text="Добавить баллы", command=save_results)
save_button.pack(pady=15)

# Таблица с рейтингами
table_frame = customtkinter.CTkFrame(root, fg_color="transparent")
table_label = customtkinter.CTkLabel(table_frame, fg_color="transparent", text="Рейтинг спортсменов", font=("Steppe", 17))
rating_table = ttk.Treeview(table_frame, columns=["#1", "#2"], show="headings" )
rating_table.heading("#1", text="Спортсмен")
rating_table.heading("#2", text="Рейтинг")
table_frame.pack()
table_label.pack()
rating_table.pack(pady=15)
update_rating_table()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Запуск основного цикла
root.mainloop()