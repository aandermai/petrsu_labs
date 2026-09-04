###########################################
# ЗАДАНИЕ 1
###########################################

def my_list(n):
    first_list = [x for x in range(n+1, 100000) if x % 724 == 0]
    second_list = first_list[49:70]
    second_list.pop(10)
    average = round(sum(second_list) / len(second_list))
    return average

###########################################
# ЗАДАНИЕ 2
###########################################

def work(n):
    set_1 = {x for x in range(2, n+1, 2)}
    set_2 = {x for x in range(5, 101, 5)}
    sum_1 = sum(set_1 | set_2)
    sum_2 = sum(set_1 & set_2)

    return sum_1 + sum_2

###########################################
# ЗАДАНИЕ 3
###########################################

def weather_forecast(day):
    weather_station1 = {
        1: [20, 735], 
        2: [21, 737], 
        3: [23, 740], 
        4: [20, 739], 
        5: [21, 750],
        6: [21, 751], 
        7: [22, 749], 
        8: [19, 745], 
        9: [22, 752],
        10: [23, 753]
    }

    weather_station2 = {
        1: [20, 89], 
        2: [20, 90], 
        3: [24, 95], 
        4: [20, 88], 
        5: [21, 87],
        6: [21, 80], 
        7: [22, 72], 
        8: [18, 80], 
        9: [22, 75],
        10: [23, 78]
    }

    temperature = (weather_station1.get(day)[0] + weather_station2.get(day)[0]) / 2
    humidity = weather_station2.get(day)[1]
    atmospheric_pressure = weather_station1.get(day)[1]

    return temperature + humidity + atmospheric_pressure

###########################################
# ЗАДАНИЕ 4
###########################################

import re

def function(string):
    pattern = r'\b[оОэЭ][а-яА-ЯёЁ]*'
    matches = re.findall(pattern, string)

    return len(matches)
###########################################
# ЗАДАНИЕ 5
###########################################

import re

def function(string):
    pattern = r'[a-zA-Zа-яА-ЯёЁ]+(?:-[a-zA-Zа-яА-ЯёЁ]+)*'
    matches = re.findall(pattern, string)

    return len(matches)
###########################################
# ЗАДАНИЕ 6
###########################################

def function(string):
    words = string.split()
    counter = 0

    for word in words:
        clean_word = word.strip(",")

        if clean_word.isupper() and len(clean_word) >= 2:
            counter += 1

    return counter
      

###########################################
# ЗАДАНИЕ 7
###########################################

def function(string):
    snake_case_string = ""

    for char in string:
        if char.isupper():
            snake_case_string += "_" + char.lower()
        else:
            snake_case_string += char

    return snake_case_string

###########################################
# ЗАДАНИЕ 8
###########################################

from datetime import datetime

def function(dt):
    time_moment = datetime.strptime('20101010 10:10:10', '%Y%m%d %H:%M:%S')
    str_to_date = datetime.strptime(dt, '%Y%m%d %H:%M:%S')
    delta = str_to_date - time_moment
    return delta.days * 24 + delta.seconds // 3600

    