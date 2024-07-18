# Работа с БД и миграциями
## Будем использовать
Будем работать с СУБД PostgreSQL, используя следующие библиотеки:
1. sqlalchemy
2. psycopg2 - коннектор с БД
3. alembic - для работы с миграциями

Миграции - это аналог системы контроля версий для БД.

## Конфигурация alembic
Первым делом выполняем команду:

`alembic init migrations`

После этого появится папка `migrations`, где будут храниться все версии базы данных, а также файл `alembic.ini`.

В файле `alembic.ini` содержится необходимая информация для доступа к базе данных: путь к ней, пароль и тд.

Но открыто держать все такие данные(пути, пароли) небезопасно. Поэтому хорошо их держать в файле .env и получать из него.

Изменим путь до базы данных:

`sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s`

### Работа с файлом .env
В файле .env перечисляем наши переменные окружения:
```commandline
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
```

Создаём скрипт config.py, который будет доставать эти переменные из файла .env при помощи модулей dotenv и os.

Затем нужно изменить скрипт env.py, находящийся в папке migrations, так, чтобы он подставил значения этих переменных в файл alembic.ini.
Для этого добавляем следующий код:
```Python
from config import DB_HOST
from models.models import metadata

section = config.config_ini_section
config.set_section_option(section, "DB_HOST", DB_HOST)

...
target_metadata = metadata
```

Настройка конфигурации alembic завершена. Теперь о том, как делать миграции: обновление базы данных и сохранение новой версии.

### Создании миграции(новой версии базы данных)
1. Создании ревизии

В командной строке пишем:
`alembic revision --autogenerate -m "message"`

В папке migrations/versions/ появится первая версия -> python скрипт

2. Делаем миграцию: `alembic upgrade <revision_hash>`
