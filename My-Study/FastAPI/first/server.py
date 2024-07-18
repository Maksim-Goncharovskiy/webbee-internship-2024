# Пусть нам нужно сделать сервер, который
# 1) содержит функциональность калькулятора - пишем запросы на выполнение операций, передавая операнды
# 2) хранит информацию о пользователях, позволяет по id пользователя получать инфомрацию о нём и менять его имя

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="MyFirstAPI") #инициализация API приложения

# Приложение FastAPI может содержать сколько угодно разделов(endpoints, эндпойнты, конечные точки),
# которые группируют функциональности приложения. Эндпойнт - URL.

# Самый главный эндпойнт - это корень приложения "/".
# К эндпойнтам обращаются обычно двумя основными методами:
# 1. get - получение информации от сервера
# 2. post - отправка данных на сервер

# Напишем функциональность для ответа на get-запрос к корню сервера:
@app.get("/")
def get_main_page_info():
    return {
        "status": 200,
        "msg": """Вы находитесь на главной странице сервера. Данное серверное приложение предоставляет следующие возможности:
        1) Калькулятор - раздел "/calculate/"
        2) Работа с пользовательскими данными - раздел "/users/"
        """
    }

# Реализуем на нашем сервере калькулятор. В разделе "/calculator/" добавим несколько функций на основные арифметические операции.
@app.get("/calculator/sum")
def summarize(first: float, second: float):
    return {
        "status": 200,
        "result": first+second
    }

@app.get("/calculator/sub")
def subtract(first: float, second: float):
    return {
        "status": 200,
        "result": first-second
    }

@app.get("/calculator/mul")
def multiply(first: float, second: float):
    return {
        "status": 200,
        "result": first*second
    }

@app.get("/calculator/div")
def divide(first: float, second: float):
    return {
        "status": 200,
        "result": first/second
    }

# Функции могут содержать параметры. Параметры как выше называются параметрами запроса.
# Они передаются в запросе к серверу.



# Теперь реализуем работу с пользователями
users_database = [
    {"id": 0, "name": "Maksim", "status": "online"},
    {"id": 1, "name": "Anya", "status": "offline"},
    {"id": 2, "name": "Ivan", "status": "online"}
]

# Первая функциональность - получение информации о пользователе через его id
@app.get('/users/{user_id}')
def get_user_id(user_id: int):
    return {
        "status": 200,
        "data": [user for user in users_database if user['id'] == user_id][0]
    }
# В примере выше user_id - это параметр URL, то есть он передаётся как часть url адреса

# Теперь напишем post метод - получение сервером данных, добавим возможность смены имени пользователя
@app.post('/users/{user_id}')
def change_user_id(user_id: int, new_name: str):
    users_database[user_id]["name"] = new_name
    return {
        "status": 200,
        "data": users_database[user_id]
    }

if __name__ == "__main__":
    uvicorn.run("first.server:app", reload=True, host="127.0.0.1", port=8000)