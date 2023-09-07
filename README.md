![restaurant_menu workflow](https://github.com/MikhailKochetkov/restaurant_menu/actions/workflows/main.yml/badge.svg?branch=main&event=push)

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)


# Описание
Меню ресторана

## Как запустить проект

Клонировать репозиторий
```bash
git clone https://github.com/MikhailKochetkov/restaurant_menu
```

Создать и активировать виртуальное окружение
```bash
python -m venv venv
source /venv/Scripts/activate
python -m pip install --upgrade pip
```

Установить зависимости из requirements.txt
```bash
pip install -r requirements.txt
```

Создать файл .env (шаблон наполнения размещен в файле .env.sample)

Создать базу данных Postgresql с именем database

Создать миграции (если необходимо)

```bash
alembic revision --autogenerate -m 'short description of migration'
```

Выполнить миграции (если необходимо)

```bash
alembic upgrade head
```

Запустить проект:
```bash
uvicorn main:app
```

### Запуск проекта в Docker (docker-compose)

Настроить sqlalchemy.url в файле alembic.ini
```bash
sqlalchemy.url = postgresql://postgres:postgres@db:5432/database
```

Настроить (проверить) значение переменной среды DB_HOST (файл .env)
```bash
DB_HOST=db
```

Собрать контейнеры
```bash
docker-compose up -d --build
```

Создать миграции (если необходимо)

```bash
docker-compose exec app alembic revision --autogenerate -m 'short description of migration'
```

Выполнить миграции (если необходимо)

```bash
docker-compose exec app alembic upgrade head
```

Остановить контейнеры
```bash
docker-compose stop
```

Остановить и удалить все контейнеры, образы, volumes
```bash
docker-compose down -v
```

### Запуск тестов в Docker (docker-compose)

Настроить (проверить) значение строки подключения к тестовой базе данных (файл db/db_connection.py)

```bash
TEST_CONNECTION_STRING = postgresql+asyncpg://postgres:postgres@test-db:5432/test_database
```

```bash
docker-compose -f docker-compose_test.yaml up
```

# Документация API
Документация доступна по эндпойнту:  http://127.0.0.1:8000/docs/

# Автор

* **Михаил Кочетков** - https://github.com/MikhailKochetkov
