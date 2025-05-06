from database import Database
from api import TaskManagerAPI
from config import DB_URL
from datetime import date

def main():
    """
    Точка входа в приложение.
    Демонстрирует использование API для работы с базой данных.
    """
    print("Инициализация системы управления задачами...")
    
    # Инициализация базы данных
    db = Database(DB_URL)
    db.create_tables()
    
    # Получение сессии БД
    session = db.get_session()
    
    # Создание API
    api = TaskManagerAPI(session)
    
    # Пример использования API
    try:
        # Создание нового пользователя
        user_id = api.create_user("Иван")
        print(f"Создан пользователь с ID: {user_id}")
        
        # Добавление идентификатора Telegram для пользователя
        api.add_user_identifier(user_id, "123456789", "telegram")
        print(f"Добавлен Telegram ID для пользователя {user_id}")
        
        # Создание регулярной задачи
        task_id = api.create_regular_task(user_id, "Зарядка", "1,2,3,4,5")  # Пн-Пт
        print(f"Создана регулярная задача с ID: {task_id}")
        
        # Создание нерегулярной задачи
        task_id2 = api.create_irregular_task(
            user_id, 
            "Подготовить отчет", 
            optimal_deadline=date(2025, 5, 10),
            hard_deadline=date(2025, 5, 15)
        )
        print(f"Создана нерегулярная задача с ID: {task_id2}")
        
        # Получение всех задач пользователя
        tasks = api.get_user_tasks(user_id)
        print(f"Задачи пользователя: {[task.name for task in tasks]}")
        
        # Получение детальной информации о задаче
        task_details = api.get_task_details(task_id)
        print(f"Детали задачи: {task_details}")
        
        # Обновление прогресса задачи
        api.update_task_progress(task_id, 50)
        print(f"Прогресс задачи {task_id} обновлен до 50%")
        
        # Проверка обновления
        task_details = api.get_task_details(task_id)
        print(f"Обновленные детали задачи: {task_details}")
        
    except Exception as e:
        print(f"Ошибка: {str(e)}")
    finally:
        session.close()
        print("Сессия закрыта")

if __name__ == "__main__":
    main()