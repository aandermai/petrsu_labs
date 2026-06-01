from pymongo import *

# Подключение к MongoDB
client = MongoClient('localhost', 27017)
db = client.internet_shop
collection = db.products

def print_query_result(query_num, description, result):
    """Вспомогательная функция для вывода результатов запросов"""
    print(f"\n{'='*60}")
    print(f"ЗАПРОС {query_num}: {description}")
    print('='*60)
    
    if isinstance(result, list):
        for item in result:
            print(item)
    elif isinstance(result, dict):
        for key, value in result:
            print(f"{key}: {value}")
    else:
        print(result)

# 1) Список названий товаров заданной категории
def get_products_by_category(category_name):
    query = {"category": category_name}
    projection = {"name": 1, "_id": 0}
    results = collection.find(query, projection)
    return [doc["name"] for doc in results]

# 2) Список характеристик (поле attributes) товаров заданной категории
def get_attributes_by_category(category_name):
    query = {"category": category_name}
    projection = {"attributes": 1, "name": 1, "_id": 0}
    results = collection.find(query, projection)
    return list(results)

# 3) Список названий и цен товаров, купленных заданным покупателем
def get_products_by_customer(customer_name):
    query = {"purchases.customerName": customer_name}
    projection = {"name": 1, "price": 1, "_id": 0}
    results = collection.find(query, projection)
    return list(results)

# 4) Список названий, производителей и цен товаров заданного цвета
def get_products_by_color(color):
    query = {"attributes.color": color}
    projection = {"name": 1, "brand": 1, "price": 1, "_id": 0}
    results = collection.find(query, projection)
    return list(results)

# 5) Общая сумма проданных товаров
def get_total_sales_amount():
    pipeline = [
        {"$unwind": "$purchases"},
        {"$project": {
            "total": {"$multiply": ["$price", "$purchases.quantity"]}
        }},
        {"$group": {
            "_id": None,
            "total_sales": {"$sum": "$total"}
        }}
    ]
    result = collection.aggregate(pipeline)
    return list(result)[0]["total_sales"]

# 6) Количество товаров в каждой категории
def get_products_count_by_category():
    pipeline = [
        {"$group": {
            "_id": "$category",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]
    results = collection.aggregate(pipeline)
    return list(results)

# 7) Список имён покупателей заданного товара
def get_customers_by_product(product_name):
    pipeline = [
        # 1. Находим нужный товар
        {"$match": {"name": product_name}},
        
        # 2. Разворачиваем массив покупок
        {"$unwind": "$purchases"},
        
        # 3. Группируем по имени покупателя (получаем уникальные имена)
        {"$group": {
            "_id": "$purchases.customerName"
        }},
        
        # 4. Преобразуем для удобного вывода
        {"$project": {
            "_id": 0,
            "customerName": "$_id"
        }},
    ]
    
    results = collection.aggregate(pipeline)
    return [doc["customerName"] for doc in results]

# 8) Список имён покупателей заданного товара с доставкой службой с заданным названием
def get_customers_by_product_and_delivery(product_name, delivery_service):
    pipeline = [
        # 1. Находим товар (уже фильтруем по доставке на уровне БД)
        {"$match": {
            "name": product_name,
            "purchases.deliveryService": delivery_service
        }},
        
        # 2. Разворачиваем массив покупок
        {"$unwind": "$purchases"},
        
        # 3. Фильтруем только покупки с нужной службой доставки
        {"$match": {
            "purchases.deliveryService": delivery_service
        }},
        
        # 4. Группируем по покупателям (уникальные имена)
        {"$group": {
            "_id": "$purchases.customerName"
        }},
        
        # 5. Форматируем результат
        {"$project": {
            "_id": 0,
            "customerName": "$_id"
        }},
    ]
    
    results = collection.aggregate(pipeline)
    return [doc["customerName"] for doc in results]






# Запрос 1
result1 = get_products_by_category("Smartphones")
print_query_result(1, "Список названий товаров категории 'Smartphones'", result1)

# Запрос 2
result2 = get_attributes_by_category("Headphones")
print_query_result(2, "Список характеристик товаров категории 'Headphones'", result2)

# Запрос 3
result3 = get_products_by_customer("Иван Иванов")
print_query_result(3, "Товары, купленные покупателем 'Иван Иванов'", result3)

# Запрос 4
result4 = get_products_by_color("Black")
print_query_result(4, "Товары черного цвета", result4)

# Запрос 5
result5 = get_total_sales_amount()
print_query_result(5, f"Общая сумма проданных товаров: ${result5}", "")

# Запрос 6
result6 = get_products_count_by_category()
print_query_result(6, "Количество товаров в каждой категории", result6)

# Запрос 7
result7 = get_customers_by_product("Sony WH-1000XM5")
print_query_result(7, "Покупатели товара 'Sony WH-1000XM5'", result7)

# Запрос 8
result8 = get_customers_by_product_and_delivery("Sony WH-1000XM5", "CDEK")
print_query_result(8, "Покупатели товара 'Sony WH-1000XM5' с доставкой CDEK", result8)

# Закрытие соединения
client.close()