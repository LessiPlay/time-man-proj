from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError
from models import User, UserID, Task, RegularTask, IrregularTask

class TaskManagerAPI:
    """
    API для работы с базой данных системы управления задачами.
    Позволяет создавать, получать, обновлять и удалять пользователей и задачи.
    """
    
    def __init__(self, db_session):
        """
        Инициализация API
        
        Args:
            db_session: Активная сессия SQLAlchemy
        """
        self.session = db_session
    
    # ======== Методы для работы с пользователями ========
    
    def create_user(self, name):
        """
        Создать нового пользователя
        
        Args:
            name (str): Имя пользователя
            
        Returns:
            int: ID созданного пользователя
            
        Raises:
            Exception: При ошибке создания пользователя
        """
        try:
            user = User(name=name)
            self.session.add(user)
            self.session.commit()
            return user.id
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при создании пользователя: {str(e)}")
    
    def add_user_identifier(self, user_id, identifier, identifier_type):
        """
        Добавить идентификатор пользователя (например, Telegram ID)
        
        Args:
            user_id (int): ID пользователя
            identifier (str): Значение идентификатора
            identifier_type (str): Тип идентификатора (например, 'telegram')
            
        Returns:
            int: ID созданного идентификатора
            
        Raises:
            Exception: При ошибке добавления идентификатора
        """
        try:
            user_id_obj = UserID(user_id=user_id, identifier=identifier, identifier_type=identifier_type)
            self.session.add(user_id_obj)
            self.session.commit()
            return user_id_obj.id
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при добавлении идентификатора пользователя: {str(e)}")
    
    def get_user_by_identifier(self, identifier, identifier_type):
        """
        Получить пользователя по его идентификатору
        
        Args:
            identifier (str): Значение идентификатора
            identifier_type (str): Тип идентификатора
            
        Returns:
            User: Объект пользователя или None, если не найден
        """
        user_id_obj = self.session.query(UserID).filter_by(
            identifier=identifier, 
            identifier_type=identifier_type
        ).first()
        
        if user_id_obj:
            return user_id_obj.user
        return None
    
    def get_user(self, user_id):
        """
        Получить пользователя по ID
        
        Args:
            user_id (int): ID пользователя
            
        Returns:
            User: Объект пользователя или None, если не найден
        """
        return self.session.query(User).filter_by(id=user_id).first()
    
    def update_user(self, user_id, name):
        """
        Обновить данные пользователя
        
        Args:
            user_id (int): ID пользователя
            name (str): Новое имя пользователя
            
        Returns:
            bool: True в случае успеха
            
        Raises:
            Exception: При ошибке обновления или если пользователь не найден
        """
        try:
            user = self.session.query(User).filter_by(id=user_id).first()
            if not user:
                raise Exception(f"Пользователь с ID {user_id} не найден")
            
            user.name = name
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при обновлении пользователя: {str(e)}")
    
    def delete_user(self, user_id):
        """
        Удалить пользователя
        
        Args:
            user_id (int): ID пользователя
            
        Returns:
            bool: True в случае успеха
            
        Raises:
            Exception: При ошибке удаления или если пользователь не найден
        """
        try:
            user = self.session.query(User).filter_by(id=user_id).first()
            if not user:
                raise Exception(f"Пользователь с ID {user_id} не найден")
            
            self.session.delete(user)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при удалении пользователя: {str(e)}")
    
    # ======== Методы для работы с задачами ========
    
    def create_task(self, user_id, name, is_regular=False):
        """
        Создать базовую задачу
        
        Args:
            user_id (int): ID пользователя
            name (str): Название задачи
            is_regular (bool): Флаг регулярности задачи
            
        Returns:
            int: ID созданной задачи
            
        Raises:
            Exception: При ошибке создания задачи
        """
        try:
            task = Task(user_id=user_id, name=name, is_regular=is_regular)
            self.session.add(task)
            self.session.commit()
            return task.id
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при создании задачи: {str(e)}")
    
    def create_regular_task(self, user_id, name, weekdays):
        """
        Создать регулярную задачу
        
        Args:
            user_id (int): ID пользователя
            name (str): Название задачи
            weekdays (str): Дни недели в формате "1,2,3,4,5,6,7"
            
        Returns:
            int: ID созданной задачи
            
        Raises:
            Exception: При ошибке создания задачи
        """
        try:
            # Создаем основную задачу
            task_id = self.create_task(user_id, name, is_regular=True)
            
            # Создаем расширенную информацию для регулярной задачи
            regular_task = RegularTask(task_id=task_id, weekdays=weekdays)
            self.session.add(regular_task)
            self.session.commit()
            
            return task_id
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при создании регулярной задачи: {str(e)}")
    
    def create_irregular_task(self, user_id, name, optimal_deadline, hard_deadline):
        """
        Создать нерегулярную задачу
        
        Args:
            user_id (int): ID пользователя
            name (str): Название задачи
            optimal_deadline (date): Оптимальный срок выполнения
            hard_deadline (date): Крайний срок выполнения
            
        Returns:
            int: ID созданной задачи
            
        Raises:
            Exception: При ошибке создания задачи
        """
        try:
            # Создаем основную задачу
            task_id = self.create_task(user_id, name, is_regular=False)
            
            # Создаем расширенную информацию для нерегулярной задачи
            irregular_task = IrregularTask(
                task_id=task_id,
                optimal_deadline=optimal_deadline,
                hard_deadline=hard_deadline
            )
            self.session.add(irregular_task)
            self.session.commit()
            
            return task_id
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при создании нерегулярной задачи: {str(e)}")
    
    def get_task(self, task_id):
        """
        Получить задачу по ID
        
        Args:
            task_id (int): ID задачи
            
        Returns:
            Task: Объект задачи или None, если не найдена
        """
        return self.session.query(Task).filter_by(id=task_id).first()
    
    def get_task_details(self, task_id):
        """
        Получить детали задачи (включая регулярную или нерегулярную информацию)
        
        Args:
            task_id (int): ID задачи
            
        Returns:
            dict: Словарь с информацией о задаче или None, если не найдена
        """
        task = self.get_task(task_id)
        if not task:
            return None
        
        result = {
            'id': task.id,
            'name': task.name,
            'progress': task.progress,
            'is_regular': task.is_regular,
            'user_id': task.user_id
        }
        
        if task.is_regular and task.regular_task:
            result['weekdays'] = task.regular_task.weekdays
        elif not task.is_regular and task.irregular_task:
            result['optimal_deadline'] = task.irregular_task.optimal_deadline
            result['hard_deadline'] = task.irregular_task.hard_deadline
        
        return result
    
    def get_user_tasks(self, user_id):
        """
        Получить все задачи пользователя
        
        Args:
            user_id (int): ID пользователя
            
        Returns:
            list: Список объектов задач
        """
        return self.session.query(Task).filter_by(user_id=user_id).all()
    
    def update_task_progress(self, task_id, progress):
        """
        Обновить прогресс выполнения задачи
        
        Args:
            task_id (int): ID задачи
            progress (int): Прогресс выполнения (0-100)
            
        Returns:
            bool: True в случае успеха
            
        Raises:
            Exception: При ошибке обновления или если задача не найдена
        """
        try:
            task = self.session.query(Task).filter_by(id=task_id).first()
            if not task:
                raise Exception(f"Задача с ID {task_id} не найдена")
            
            task.progress = progress
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при обновлении прогресса задачи: {str(e)}")
    
    def update_regular_task(self, task_id, name=None, weekdays=None):
        """
        Обновить регулярную задачу
        
        Args:
            task_id (int): ID задачи
            name (str, optional): Новое название задачи
            weekdays (str, optional): Новые дни недели
            
        Returns:
            bool: True в случае успеха
            
        Raises:
            Exception: При ошибке обновления или если задача не найдена
        """
        try:
            regular_task = self.session.query(RegularTask).filter_by(task_id=task_id).first()
            if not regular_task:
                raise Exception(f"Регулярная задача с task_id {task_id} не найдена")
            
            if name:
                # Также обновляем основную задачу
                task = self.session.query(Task).filter_by(id=task_id).first()
                task.name = name
            
            if weekdays:
                regular_task.weekdays = weekdays
            
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при обновлении регулярной задачи: {str(e)}")
    
    def update_irregular_task(self, task_id, name=None, optimal_deadline=None, hard_deadline=None):
        """
        Обновить нерегулярную задачу
        
        Args:
            task_id (int): ID задачи
            name (str, optional): Новое название задачи
            optimal_deadline (date, optional): Новый оптимальный срок
            hard_deadline (date, optional): Новый крайний срок
            
        Returns:
            bool: True в случае успеха
            
        Raises:
            Exception: При ошибке обновления или если задача не найдена
        """
        try:
            irregular_task = self.session.query(IrregularTask).filter_by(task_id=task_id).first()
            if not irregular_task:
                raise Exception(f"Нерегулярная задача с task_id {task_id} не найдена")
            
            if name:
                # Обновляем основную задачу
                task = self.session.query(Task).filter_by(id=task_id).first()
                task.name = name
            
            if optimal_deadline:
                irregular_task.optimal_deadline = optimal_deadline
            
            if hard_deadline:
                irregular_task.hard_deadline = hard_deadline
            
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при обновлении нерегулярной задачи: {str(e)}")
    
    def delete_task(self, task_id):
        """
        Удалить задачу
        
        Args:
            task_id (int): ID задачи
            
        Returns:
            bool: True в случае успеха
            
        Raises:
            Exception: При ошибке удаления или если задача не найдена
        """
        try:
            task = self.session.query(Task).filter_by(id=task_id).first()
            if not task:
                raise Exception(f"Задача с ID {task_id} не найдена")
            
            self.session.delete(task)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Ошибка при удалении задачи: {str(e)}")