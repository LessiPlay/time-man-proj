# Система управления задачами - API для базы данных

API для работы с базой данных задач пользователей. Позволяет создавать, получать, обновлять и удалять пользователей и их задачи (регулярные и нерегулярные).

## Структура базы данных

- **Users**: Хранит информацию о пользователях
- **UserIDs**: Хранит идентификаторы пользователей (например, telegram_id)
- **Tasks**: Основная таблица с задачами
- **RegularTasks**: Расширение для регулярных задач (с днями недели)
- **IrregularTasks**: Расширение для нерегулярных задач (с дедлайнами)

## Установка и настройка

### Предварительные требования

- Python 3.8+
- PostgreSQL

### Шаги установки

1. Клонируйте репозиторий

2. Активируйте venv

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` на основе примера:
   ```
   cp .env.example .env
   ```

5. Отредактируйте файл `.env` и укажите настройки вашей базы данных:
   ```
   DB_USER=ваш_пользователь
   DB_PASSWORD=ваш_пароль
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=task_manager
   ```

6. Создайте бд, например
    ```
    podman run -d \
    --name postgres \
    -e POSTGRES_DB=task_manager \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=mypassword \
    -p 5432:5432 \
    docker.io/library/postgres:16
    ```

7. Запустите приложение для создания таблиц и тестирования:
   ```
   python main.py
   ```

## Использование API

### Инициализация API

```python
from database import Database
from api import TaskManagerAPI
from config import DB_URL

# Инициализация базы данных
db = Database(DB_URL)
db.create_tables()

# Получение сессии БД
session = db.get_session()

# Создание API
api =