# API для работы с пользовательскими данными. Уделим особое внимание валидации данных.
from fastapi import FastAPI
import uvicorn

users_database = [
    {"id": 0, "name": "Maksim", "age": 19, "level": "junior"},
    {"id": 1, "name": "Anya", "age": 20, "level": "middle"},
    {"id": 2, "name": "Ivan", "age": 33, "level": "senior", "achievements": ["Good"]}
]

app = FastAPI(title="ValidationTrain")

# Добавим возможность добавления нескольких новых пользователей
# Можно валидировать типы каждого поля: id: int, name: str ... <- Но это неудобно и не очень гибко(нельзя ограничить значения)

from pydantic import BaseModel # <- для создания классов, задающих формат
from pydantic import Field # <- для ограничения значений полей
from enum import Enum # <- для описания перечислений(поле принимает только определенные конечные значения)
from typing import List
from typing import Optional # <- сделать данное поле опциональным(необязательным)


class LevelType(Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"


class User(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(max_length=100, min_length=2)
    age: int = Field(ge=14)
    level: LevelType
    achievements: Optional[List[str]] = []



@app.post("/admin/users")
def add_new_users(users: List[User]):
    users_database.extend(users)
    return {
        "status": 200,
        "data": users_database
    }


# Валидация исходящих данных: проверка того, что отправляемые сервером данные соответствуют ожидаемому формату.
# Делается это при помощи аргумента response_model=...
class GoodResponse(BaseModel):
    status: int
    data: List[User]

@app.get("/admin/users", response_model=GoodResponse)
def get_all_users():
    return {
        "status": 200,
        "data": users_database
    }

if __name__ == "__main__":
    uvicorn.run("second.server:app", reload=True, host="127.0.0.1", port=8001)