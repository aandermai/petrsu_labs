import customtkinter
from tkinter import *
from tkinter import font
from tkinter.messagebox import showerror, showwarning, showinfo
import redis

# Функция для получения настроек пользователя и их применения к надписи
def get_inscription_settings(event):
    inscription_settings = setting_entry.get().split(", ") # Получение настроек

    # Проверки на правильность ввода настроек и их применение
    if (len(inscription_settings) == 4 and inscription_settings[0] in FONTS and
            inscription_settings[3].lower() in STYLES):
            output_inscription.configure(font=(inscription_settings[0], int(inscription_settings[1]), inscription_settings[3]),
                                        text_color=inscription_settings[2].lower())
    else:
        showwarning(title="Предупреждение", message="Настройки не были применены, так как не введены все данные или некоторые данные введены неверно")

# Функция для сохранения пользовательских настроек в базе данных
def save_settings():
    inscription_settings = setting_entry.get().split(", ") # Введённые настройки
    settings_username = user_combobox.get() # Имя пользователя

    # Проверка на верное количество аргументов в настройках
    if len(inscription_settings) != 4:
        showerror(title="Ошибка", message="Не введены все данные для форматирования надписи")
        return
    
    # Проверка на непустое имя пользователя в комбобоксе
    if settings_username == "":
        showerror(title="Ошибка", message="Не введено имя пользователя для сохранения настроек")
        return
    
    # Проверка правильности ввода и компановка словаря с настройками
    if (inscription_settings[0] in FONTS and (inscription_settings[1].isdigit()) and 
            inscription_settings[3].lower() in STYLES):
        user_settings = {
            "font-name": inscription_settings[0],
            "font-size": inscription_settings[1],
            "font-color": inscription_settings[2],
            "font-style": inscription_settings[3]
        }

        # Меняем значение ключа
        r.hset(settings_username, mapping=user_settings)

        # Обновляем комбобокс с пользователями
        showinfo(title="Информация", message="Настройки успешно сохранены")
        user_combobox.configure(values=r.keys("*"))
    else:
        showerror(title="Ошибка", message="Некоторые данные введены некорректно")
        return

# Функция для добавления пользователя в БД
def add_user():
    default_settings = {"font-name": "Arial", "font-size": "12", "font-color": "black", "font-style": "normal"}
    user = name_entry.get()

    if user == "":
        showerror(title="Ошибка", message="Не введено имя пользователя")
        return

    r.hset(user, mapping=default_settings)
    showinfo(title="Информация", message="Пользователь успешно добавлен")
    user_combobox.configure(values=r.keys("*"))

# Функция для выбора настроек пользователей и применения их
def select_settings(user):
    settings = f'{r.hget(user, "font-name")}, {r.hget(user, "font-size")}, {r.hget(user, "font-color")}, {r.hget(user, "font-style")}'
    setting_entry.delete(0, END)
    setting_entry.insert(0, settings)
    setting_entry.focus_set()
    setting_entry.event_generate('<Return>')

# Подключение к БД и проверка на подключение
r = redis.StrictRedis(host="127.0.0.1", port=6379, password="student", decode_responses=True, db=0)
print(f'Результат подключения: {r.ping()}')

# Основные настройки окна
root = customtkinter.CTk()
root.geometry("1000x500")
root.title("Форматирование надписей")

FONTS = font.families() # Шрифты
STYLES = ["normal", "bold", "italic", "overstrike", "underline"] # Начертания

# Левый фрейм
left_frame = customtkinter.CTkFrame(root, fg_color="transparent")
left_frame.pack(side=LEFT, padx=100, fill=BOTH)

# Поле ввода для настроек пользователя
setting_frame = customtkinter.CTkFrame(left_frame, width=300, fg_color="transparent")
setting_label = customtkinter.CTkLabel(setting_frame, text="Настройки текста", width=300, font=("Steppe", 17))
setting_entry = customtkinter.CTkEntry(setting_frame, placeholder_text="Пример: Arial, 12, Black, Bold", width=300)
instruction_label = customtkinter.CTkLabel(setting_frame, text="Порядок ввода: Шрифт, размер, цвет, начертание", font=("Steppe", 12))
setting_frame.pack(pady=40)
setting_label.pack()
setting_entry.pack()
instruction_label.pack()

# Обработка события при нажатии на Enter в поле ввода пользовательских настроек
setting_entry.bind("<Return>", get_inscription_settings)

# Поле ввода для имени пользователя, чтобы сохранить настройки
name_frame = customtkinter.CTkFrame(left_frame, width=300, fg_color="transparent")
name_label = customtkinter.CTkLabel(name_frame, text="Новый пользователь", font=("Steppe", 17))
name_entry = customtkinter.CTkEntry(name_frame, width=300, placeholder_text="Например: Артем Петрушин")
name_frame.pack(pady=15)
name_label.pack()
name_entry.pack()

# Кнопка добавления пользователя
add_button = customtkinter.CTkButton(name_frame, text="Добавить пользователя", command=add_user)
add_button.pack(pady=15, padx=100)

# Выпадающий список для выбора пользователя
user_frame = customtkinter.CTkFrame(left_frame, width=300, fg_color="transparent")
user_label = customtkinter.CTkLabel(user_frame, text="Пользователь", font=("Steppe", 17))
user_combobox = customtkinter.CTkComboBox(user_frame, values=r.keys("*"), width=300, command=select_settings)
user_combobox.set("")
user_frame.pack(pady=15)
user_label.pack()
user_combobox.pack()

# Кнопка сохранения настроек
save_button = customtkinter.CTkButton(user_frame, text="Сохранить настройки", command=save_settings)
save_button.pack(pady=15, padx=100, anchor=SW, side=BOTTOM)

# Правый фрейм
right_frame = customtkinter.CTkFrame(root, fg_color="transparent")
right_frame.pack(side=RIGHT, padx=100, fill=BOTH)

# Поле ввода для надписи
inscription = StringVar()
inscription_frame = customtkinter.CTkFrame(right_frame, width=300, fg_color="transparent")
inscription_label = customtkinter.CTkLabel(inscription_frame, fg_color="transparent", text="Текст", font=("Steppe", 17))
inscription_entry = customtkinter.CTkEntry(inscription_frame, textvariable=inscription, width=300)
inscription_frame.pack(pady=40)
inscription_label.pack()
inscription_entry.pack()

# Отформатированная надпись
output_inscription_frame = customtkinter.CTkFrame(right_frame, fg_color="transparent", width=300)
output_inscription_label = customtkinter.CTkLabel(output_inscription_frame, text="Предосмотр", fg_color="transparent", font=("Steppe", 17))
output_inscription = customtkinter.CTkLabel(output_inscription_frame, textvariable=inscription, font=("Arial", 12, "bold"), width=300, height=120, fg_color="white", text_color="black")
output_inscription_frame.pack(pady=30)
output_inscription_label.pack()
output_inscription.pack()

# Запуск основного цикла
root.mainloop()