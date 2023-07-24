![restaurant_menu workflow](https://github.com/MikhailKochetkov/restaurant_menu/actions/workflows/main.yml/badge.svg?branch=main&event=push)

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)


# Описание
Меню ресторана

## Как запустить проект:

Клонировать репозиторий:
```bash
git clone https://github.com/MikhailKochetkov/restaurant_menu
```

Создать и активировать виртуальное окружение:
```bash
python -m venv venv
source /venv/Scripts/activate
python -m pip install --upgrade pip
```

Установить зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```

Создать файл .env (шаблон наполнения размещен в файле .env.sample)

### Запуск проекта в режиме разработки (БД SQLite):

Установить режим разработчика в настройках проекта (файл settings.py):
```bash
DEV_MODE = True
```

Запустить проект:
```bash
uvicorn main:app
```

### Запуск проекта в режиме разработки (БД Postgresql):

Создать базу данных с именем database

Настроить режим разработчика в настройках проекта (файл settings.py):
```bash
DEV_MODE = False
```

Настроить (проверить) значение переменной среды DB_HOST (файл .env):
```bash
DB_HOST=localhost
```

Запустить проект:
```bash
uvicorn main:app
```

### Запуск проекта в Docker (dockerfile, БД SQLite):

Настроить режим разработчика в настройках проекта (файл settings.py):
```bash
DEV_MODE = True
```

Собрать образ:
```bash
docker build -t api .
```

Запустить контейнер:
```bash
docker run --name restaurant_menu -it -p 8000:8000 api
```

Получить ID запущенного контейнера:
```bash
docker container ls
```

Остановить контейнер:
```bash
docker container stop <CONTAINER ID>
```

### Запуск проекта в Docker (docker-compose, БД Postgresql):

Настроить режим разработчика в настройках проекта (файл settings.py):
```bash
DEV_MODE = False
```

Настроить (проверить) значение переменной среды DB_HOST (файл .env):
```bash
DB_HOST=db
```

Собрать контейнеры:
```bash
docker-compose up -d --build
```

Остановить контейнеры:
```bash
docker-compose stop
```

Остановить и удалить все контейнеры, образы, volumes:
```bash
docker-compose down -v
```

# Документация API
Документация доступна по эндпойнту:  http://127.0.0.1:8000/docs/

# Автор

* **Михаил Кочетков** - https://github.com/MikhailKochetkov