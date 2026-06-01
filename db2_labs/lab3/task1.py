from customtkinter import *
from pymongo import *
import tkinter.ttk as ttk
from tkinter.messagebox import showerror, showinfo
import json
from bson.objectid import ObjectId
from datetime import datetime

# Агрегация mingoals
def min_goals_aggregate():
    def execute_aggregation():
        # Получаем значения из полей
        min_goals = min_goals_entry.get()
        date_from_str = date_from_entry.get()
        date_to_str = date_to_entry.get()
        limit = limit_entry.get()
        
        # Валидация minGoals
        if not min_goals:
            showerror("Ошибка", "Введите minGoals (целое число ≥ 0)")
            return
            
        try:
            min_goals = int(min_goals)
            if min_goals < 0:
                showerror("Ошибка", "minGoals должно быть ≥ 0")
                return
        except ValueError:
            showerror("Ошибка", "minGoals должно быть целым числом")
            return
        
        # Преобразование дат
        date_from = None
        date_to = None
        
        if date_from_str:
            try:
                date_from = datetime.strptime(date_from_str, "%Y-%m-%d")
            except ValueError:
                showerror("Ошибка", "Некорректный формат даты (dateFrom). Используйте YYYY-MM-DD")
                return
        
        if date_to_str:
            try:
                date_to = datetime.strptime(date_to_str, "%Y-%m-%d")
                # Добавляем время конца дня
                date_to = date_to.replace(hour=23, minute=59, second=59)
            except ValueError:
                showerror("Ошибка", "Некорректный формат даты (dateTo). Используйте YYYY-MM-DD")
                return
        
        # Преобразование лимита
        limit = None
        if limit_entry.get():  # Проверяем, есть ли текст в поле ввода
            limit_str = limit_entry.get()
            try:
                limit = int(limit_str)
                if limit <= 0:
                    showerror("Ошибка", "limit должен быть > 0")
                    return
            except ValueError:
                showerror("Ошибка", "limit должен быть целым числом")
                return
        
        # Очищаем таблицу результатов
        for item in results_table.get_children():
            results_table.delete(item)
        
        try:
            # Строим конвейер агрегации
            pipeline = []
            
            # Этап 1: Фильтрация по датам (если указаны)
            if date_from or date_to:
                date_filter = {}
                if date_from:
                    date_filter["$gte"] = date_from
                if date_to:
                    date_filter["$lte"] = date_to
                pipeline.append({"$match": {"date": date_filter}})
            
            # Этап 2: Разворачиваем массив голов
            pipeline.append({"$unwind": "$goals"})
            
            # Этап 4: Группируем по автору голов, считаем голы
            pipeline.append({
                "$group": {
                    "_id": "$goals.author",  # Группируем по автору гола
                    "goals": {"$sum": 1}     # Считаем количество голов
                }
            })
            
            # Этап 5: Фильтруем по minGoals (строго больше)
            pipeline.append({
                "$match": {
                    "goals": {"$gt": min_goals}
                }
            })
            
            # Этап 6: Сортируем по количеству голов 
            pipeline.append({
                "$sort": {"goals": -1}
            })
            
            # Этап 7: Проекция для результата
            pipeline.append({
                "$project": {
                    "player": "$_id",  # Переименовываем _id в player для отображения
                    "goals": 1,
                    "_id": 0
                }
            })
            
            # Этап 8: Лимит (если указан)
            if limit:
                pipeline.append({"$limit": limit})
            
            # Выполняем агрегацию
            collection = db["games"]
            results = list(collection.aggregate(pipeline))

            
            if not results:
                showinfo("Результат", "Игроки с таким количеством голов не найдены")
                return
            
            # Заполняем таблицу результатами
            for result in results:
                player = result.get("player", "Неизвестный")
                goals = result.get("goals", 0)
                results_table.insert("", END, values=[player, goals])
            
            showinfo("Успех", f"Найдено игроков: {len(results)}")
            
        except Exception as e:
            showerror("Ошибка", f"Ошибка при выполнении агрегации: {str(e)}")
        
    # Создание окна агрегации
    window = CTkToplevel(root)
    window.geometry("700x500")
    window.title("Агрегация: игроки с числом голов > minGoals")
    window.transient(root)
    
    # Основной фрейм
    main_frame = CTkFrame(window, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Заголовок
    title_label = CTkLabel(main_frame, text="Игроки с числом голов > minGoals", 
                          font=("Steppe", 20, "bold"))
    title_label.pack(anchor="w", pady=(0, 20))
    
    # Фрейм для параметров
    params_frame = CTkFrame(main_frame, fg_color="transparent")
    params_frame.pack(fill="x", pady=(0, 20))
    
    # Поле minGoals (обязательное)
    min_goals_label = CTkLabel(params_frame, text="minGoals *", font=("Steppe", 14))
    min_goals_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
    min_goals_entry = CTkEntry(params_frame, width=200)
    min_goals_entry.grid(row=1, column=0, sticky="w", pady=(0, 15))
    
    # Поле dateFrom (необязательное)
    date_from_label = CTkLabel(params_frame, text="dateFrom (YYYY-MM-DD)", font=("Steppe", 14))
    date_from_label.grid(row=0, column=1, sticky="w", padx=(20, 0), pady=(0, 5))
    date_from_entry = CTkEntry(params_frame, width=200, 
                              placeholder_text="например: 2023-01-01")
    date_from_entry.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=(0, 15))
    
    # Поле dateTo (необязательное)
    date_to_label = CTkLabel(params_frame, text="dateTo (YYYY-MM-DD)", font=("Steppe", 14))
    date_to_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
    date_to_entry = CTkEntry(params_frame, width=200, 
                            placeholder_text="например: 2023-12-31")
    date_to_entry.grid(row=3, column=0, sticky="w", pady=(0, 15))
    
    # Поле limit (необязательное)
    limit_label = CTkLabel(params_frame, text="limit", font=("Steppe", 14))
    limit_label.grid(row=2, column=1, sticky="w", padx=(20, 0), pady=(0, 5))
    limit_entry = CTkEntry(params_frame, width=200, 
                          placeholder_text="например: 10")
    limit_entry.grid(row=3, column=1, sticky="w", padx=(20, 0), pady=(0, 15))
    
    # Кнопка выполнения
    execute_btn = CTkButton(main_frame, text="Выполнить агрегацию", 
                           command=execute_aggregation,
                           height=40, font=("Steppe", 14))
    execute_btn.pack(fill="x", pady=(0, 20))
    
    # Заголовок таблицы результатов
    results_label = CTkLabel(main_frame, text="Результаты", font=("Steppe", 16))
    results_label.pack(anchor="w", pady=(0, 10))
    
    # Фрейм для таблицы результатов
    table_frame = CTkFrame(main_frame, fg_color="transparent")
    table_frame.pack(fill="both", expand=True)
    
    # Таблица результатов
    results_table = ttk.Treeview(table_frame, 
                                columns=("player", "goals"), 
                                show="headings",
                                height=10)
    
    # Настройка колонок
    results_table.column("player", width=300, anchor="w")
    results_table.column("goals", width=100, anchor="center")
    
    results_table.heading("player", text="Игрок")
    results_table.heading("goals", text="Голы")
    
    # Добавляем скроллбар
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=results_table.yview)
    results_table.configure(yscrollcommand=scrollbar.set)
    
    results_table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Окно поиска
def search_window():
    def search(): 
        key = key_entry.get()
        symbol = symbol_combobox.get()
        value = value_entry.get()
        collection_name = collection_combobox.get()
        
        if not collection_name:
            showerror("Ошибка", "Выберите коллекцию")
            return
            
        if not key:
            showerror("Ошибка", "Введите ключ для поиска")
            return
            
        if not symbol:
            showerror("Ошибка", "Выберите оператор сравнения")
            return
            
        if value == "":
            showerror("Ошибка", "Введите значение для поиска")
            return
        
        collection = db[collection_name]
        
        # Преобразуем значение в правильный тип
        converted_value = value
        
        # Пробуем преобразовать в число
        try:
            if '.' in value:
                converted_value = float(value)
            else:
                converted_value = int(value)
        except ValueError:
            # Если не число, проверяем на булево значение
            if value.lower() == 'true':
                converted_value = True
            elif value.lower() == 'false':
                converted_value = False
            elif value.lower() == 'null' or value.lower() == 'none':
                converted_value = None
            # Иначе оставляем строкой
        
        # Формируем запрос в зависимости от оператора
        query = {}
        
        if symbol == ">":
            query = {key: {"$gt": converted_value}}
        elif symbol == "<":
            query = {key: {"$lt": converted_value}}
        elif symbol == ">=":
            query = {key: {"$gte": converted_value}}
        elif symbol == "<=":
            query = {key: {"$lte": converted_value}}
        elif symbol == "=":
            query = {key: converted_value}
        
        try:
            # Выполняем поиск
            results = list(collection.find(query))
            
            # Очищаем таблицу
            for item in search_results_table.get_children():
                search_results_table.delete(item)
            
            if not results:
                showinfo("Результат", "Документы не найдены")
                return
            
            for document in results:
                # Преобразуем документ для отображения
                doc_copy = document.copy()
                doc_copy['_id'] = str(doc_copy['_id'])
                
                # Форматируем для отображения
                doc_str = json.dumps(doc_copy, ensure_ascii=False, default=str)
                
                # Сохраняем полный документ в теге
                search_results_table.insert("", END, values=[doc_str])
                
            showinfo("Успех", f"Найдено документов: {len(results)}")
            
        except Exception as e:
            showerror("Ошибка поиска", f"Ошибка при выполнении поиска: {str(e)}\n"
                                      f"Проверьте корректность ключа: {key}")


    # Создание окна
    window = CTkToplevel(root)
    window.geometry("1000x500")
    window.title("Поиск")
    window.transient(root)

    # Создаем основной фрейм для разделения на левую и правую части
    main_frame = CTkFrame(window, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ЛЕВАЯ ЧАСТЬ - поля и кнопки
    left_frame = CTkFrame(main_frame, width=400, fg_color="transparent")
    left_frame.pack(side="left", fill="both", padx=(0, 10))
    left_frame.pack_propagate(False)

    # Выбор коллекции
    collection_label = CTkLabel(left_frame, text="Коллекция", font=("Steppe", 17))
    collection_label.pack(anchor="w", pady=(10, 5))
    collection_combobox = CTkComboBox(left_frame, values=db.list_collection_names())
    collection_combobox.set("")
    collection_combobox.pack(fill="x", pady=(0, 10))

    # Поле ввода ключа
    key_label = CTkLabel(left_frame, text="Ключ", font=("Steppe", 17), fg_color="transparent")
    key_label.pack(anchor="w", pady=(10, 5))
    
    key_entry = CTkEntry(left_frame)
    key_entry.pack(fill="x", pady=(0, 10))

    # Поле выбора знака
    symbol_label = CTkLabel(left_frame, text="Оператор", font=("Steppe", 17), fg_color="transparent")
    symbol_label.pack(anchor="w", pady=(10, 5))
    
    symbol_combobox = CTkComboBox(left_frame, values=[">", ">=", "=", "<=", "<"])
    symbol_combobox.set("")
    symbol_combobox.pack(fill="x", pady=(0, 10))

    # Поле ввода значения
    value_label = CTkLabel(left_frame, text="Значение", font=("Steppe", 17), fg_color="transparent")
    value_label.pack(anchor="w", pady=(10, 5))
    
    value_entry = CTkEntry(left_frame)
    value_entry.pack(fill="x", pady=(0, 10))

    # Фрейм для кнопок
    button_frame = CTkFrame(left_frame, fg_color="transparent")
    button_frame.pack(fill="x", pady=10)

    # Кнопка поиска
    search_btn = CTkButton(button_frame, text="Искать", command=search)
    search_btn.pack(side="top", fill="x", pady=5)

    # ПРАВАЯ ЧАСТЬ - список результатов
    right_frame = CTkFrame(main_frame, fg_color="transparent")
    right_frame.pack(side="right", fill="both", expand=True)

    # Заголовок результатов
    results_label = CTkLabel(right_frame, text="Результаты поиска", font=("Steppe", 20))
    results_label.pack(anchor="w", pady=(0, 10))

    # Создаем фрейм для Treeview и скроллбара
    tree_frame = CTkFrame(right_frame, fg_color="transparent")
    tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

    # Treeview для отображения результатов
    search_results_table = ttk.Treeview(tree_frame, columns=("result"), show="headings", height=20)

    # Настраиваем ширину колонок
    search_results_table.column("result", width=200)
    search_results_table.heading(column="result", text="Найденные документы")

    # Упаковываем Treeview
    search_results_table.pack(side="left", fill="both", expand=True)

# Функция для выбора документа при нажатии на него в списке
def choose_document(event):
    global current_document
    item_id = document_table.focus()
    if not item_id:
        return
    
    item_data = document_table.item(item_id)
    values = item_data['values']
    
    if values and len(values) > 0:
        # Получаем строку JSON и преобразуем в словарь
        doc_str = values[0]
        current_document = json.loads(doc_str)
        
        # Преобразуем строковый _id в ObjectId для корректной работы с MongoDB
        if '_id' in current_document and isinstance(current_document['_id'], str):
            try:
                current_document['_id'] = ObjectId(current_document['_id'])
            except:
                pass
        
        print(f"Выбран документ с _id: {current_document.get('_id')}")
    
    return current_document

# Функция создания документа
def create_document():
    global current_document

    # Получение имени коллекции
    collection_entry = collection_combobox.get() 
    if collection_entry == "":
        showerror(title="Ошибка", message="Не выбрана коллекция для создания документа")
        return 

    collection = db[collection_entry] # Выбор коллекции в БД
    result = collection.insert_one({}) # Вставляем пустой документ
    
    # Устанавливаем текущий документ с корректным _id
    current_document = {'_id': result.inserted_id}
    
    show_documents()
    
    # Находим и выделяем новый документ в таблице
    for item in document_table.get_children():
        item_data = document_table.item(item)
        values = item_data['values']
        if values and len(values) > 0:
            doc = json.loads(values[0])
            if str(doc['_id']) == str(result.inserted_id):
                document_table.focus(item)
                document_table.selection_set(item)
                break

# Функция добавления ключа-значения
def add_key_value():
    global current_document
    
    key = key_entry.get()
    value = value_entry.get()
    
    if key == "" or value == "":
        showerror(title="Ошибка", message="Не заполнено поле ключа или значения")
        return 
    
    if current_document is None or '_id' not in current_document:
        showerror(title="Ошибка", message="Сначала создайте или выберите документ")
        return
    
    # Преобразуем значение в правильный тип
    converted_value = value
    
    try:
        if '.' in value:
            converted_value = float(value)
        else:
            converted_value = int(value)
    except ValueError:
        if value.lower() == 'true':
            converted_value = True
        elif value.lower() == 'false':
            converted_value = False
        elif value.lower() == 'null' or value.lower() == 'none':
            converted_value = None
    
    try:
        # Если есть точка - используем dot notation
        if '.' in key:
            # Но для локального документа создадим вложенную структуру
            keys = key.split('.')
            current = current_document
            
            # Проходим по всем ключам кроме последнего
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            # Устанавливаем значение для последнего ключа
            current[keys[-1]] = converted_value
        else:
            # Простое поле
            current_document[key] = converted_value
            
    except Exception as e:
        showerror(title="Ошибка", message=f"Не удалось добавить поле: {str(e)}")
        return
    
    # Очищаем поля ввода
    key_entry.delete(0, END)
    value_entry.delete(0, END)
    
    print(f"Добавлено поле: {key} = {converted_value}")
    print(f"Текущий документ: {json.dumps(current_document, default=str, ensure_ascii=False)}")

# Функция сохранения документа
def save_document():
    global current_document # Локальная копия документа
    
    # Проверка на существование документа для сохранения
    if current_document is None or '_id' not in current_document:
        showerror(title="Ошибка", message="Нет документа для сохранения. Сначала создайте или выберите документ.")
        return
    
    # Получение имени коллекции
    collection_name = collection_combobox.get()
    if collection_name == "":
        showerror(title="Ошибка", message="Не выбрана коллекция")
        return
        
    collection = db[collection_name] # Выбор коллекции в БД
    
    # Получаем _id документа
    doc_id = current_document['_id']
    
    # Удаляем _id из документа для обновления
    document_to_update = current_document.copy()
    del document_to_update['_id']
    
    # Обновляем документ в базе данных
    try:
        result = collection.update_one(
            {'_id': doc_id},
            {'$set': document_to_update},
            upsert=False
        )
        
        # Проверяем результат
        if result.matched_count == 0:
            showerror(title="Ошибка", message="Документ не найден в базе данных")
        elif result.modified_count > 0:
            showinfo(title="Успех", message="Документ успешно сохранен")
        else:
            showinfo(title="Информация", message="Документ уже актуален, изменений не требуется")
    
    except Exception as e:
        showerror(title="Ошибка", message=f"Ошибка при сохранении: {str(e)}")
    
    # Сбрасываем текущий документ
    current_document = None
    
    # Обновляем таблицу со списком документов
    show_documents()

# Функция показа документов
def show_documents():
    # Очищаем таблицу
    for item in document_table.get_children():
        document_table.delete(item)
    
    # Получение имени коллекции
    collection_name = collection_combobox.get()
    if collection_name == "":
        return
    
    try:
        collection = db[collection_name] # Выбор коллекции в БД
        documents = list(collection.find({})) # Получение списка всех документов коллекции
        
        for doc in documents:
            # Преобразуем ObjectId в строку
            doc_copy = doc.copy()
            doc_copy['_id'] = str(doc_copy['_id'])
            
            # Преобразуем в JSON строку и вставляем всё в таблицу
            doc_str = json.dumps(doc_copy, ensure_ascii=False, default=str)
            document_table.insert("", END, values=[doc_str])
            
    except Exception as e:
        print(f"Ошибка при получении документов: {e}")

# Подключение к БД
client = MongoClient('localhost', 27017)
db = client.football_db # Выбор БД
current_document = None # Документ, который сейчас редактируется

# Создание окна
root = CTk()
root.geometry("1000x500")
root.title("Футбольные команды и матчи")

# Создаем основной фрейм для разделения на левую и правую части
main_frame = CTkFrame(root, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ЛЕВАЯ ЧАСТЬ - поля и кнопки
left_frame = CTkFrame(main_frame, width=400, fg_color="transparent")
left_frame.pack(side="left", fill="both", padx=(0, 10))
left_frame.pack_propagate(False) 

# Выбор коллекции
collection_label = CTkLabel(left_frame, text="Коллекция", font=("Steppe", 17))
collection_label.pack(anchor="w", pady=(10, 5))
collection_combobox = CTkComboBox(left_frame, values=db.list_collection_names())
collection_combobox.set("")
collection_combobox.pack(fill="x", pady=(0, 10))

# Текстовое поле ввода ключа
key_entry_label = CTkLabel(left_frame, text="Ключ", font=("Steppe", 17), fg_color="transparent")
key_entry_label.pack(anchor="w", pady=(10, 5))
key_entry = CTkEntry(left_frame)
key_entry.pack(fill="x", pady=(0, 10))

# Текстовое поле ввода значения
value_entry_label = CTkLabel(left_frame, text="Значение", font=("Steppe", 17), fg_color="transparent")
value_entry_label.pack(anchor="w", pady=(10, 5))
value_entry = CTkEntry(left_frame)
value_entry.pack(fill="x", pady=(0, 10))

# Фрейм для кнопок
button_frame = CTkFrame(left_frame, fg_color="transparent")
button_frame.pack(fill="x", pady=10)

# Кнопка "Создать документ"
create_document_btn = CTkButton(button_frame, text="Создать документ", command=create_document)
create_document_btn.pack(side="top", fill="x", pady=5)

# Кнопка "Добавить ключ-значение"
add_key_value_btn = CTkButton(button_frame, text="Добавить ключ-значение", command=add_key_value)
add_key_value_btn.pack(side="top", fill="x", pady=5)

# Кнопка "Сохранить документ"
save_document_btn = CTkButton(button_frame, text="Сохранить документ", command=save_document)
save_document_btn.pack(side="top", fill="x", pady=5)

# Кнопка "Показать документы"
show_documents_btn = CTkButton(button_frame, text="Показать документы", command=show_documents)
show_documents_btn.pack(side="top", fill="x", pady=5)


aggregate_btn = CTkButton(left_frame, text="Агрегация: игроки с голами", command=min_goals_aggregate)
aggregate_btn.pack(side="bottom", fill="x")

# Кнопка открытия окна поиска
search_window_btn = CTkButton(left_frame, text="Открыть окно поиска", command=search_window)
search_window_btn.pack(side="bottom", fill="x", pady=(0, 10))

# ПРАВАЯ ЧАСТЬ - список документов
right_frame = CTkFrame(main_frame, fg_color="transparent")
right_frame.pack(side="right", fill="both", expand=True)

# Заголовок для списка документов
docs_label = CTkLabel(right_frame, text="Документы коллекции", font=("Steppe", 20))
docs_label.pack(anchor="w", pady=(0, 10))

# Создаем фрейм для Treeview и скроллбаров
tree_container = CTkFrame(right_frame, fg_color="transparent")
tree_container.pack(fill="both", expand=True, padx=5, pady=5)

# Создаем Treeview с фиксированной шириной
document_table = ttk.Treeview(tree_container, columns=("content"), show="headings", height=20)

# Настраиваем колонку с минимальной шириной больше фрейма
document_table.column("content", width=650)  # Фиксированная ширина больше контейнера
document_table.heading(column="content", text="Документы")
document_table.pack(side="top", fill="both", expand=True)

# Бинд на левую кнопку мышки
document_table.bind('<ButtonRelease-1>', choose_document)

# Запуск основного цикла
root.mainloop()