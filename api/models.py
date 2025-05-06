from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Создаем базовый класс для моделей
Base = declarative_base()

class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    # Связь с идентификаторами пользователя
    identifiers = relationship("UserID", back_populates="user", cascade="all, delete-orphan")
    # Связь с задачами пользователя
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

class UserID(Base):
    """Модель идентификаторов пользователя (например, telegram_id)"""
    __tablename__ = "user_ids"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    identifier = Column(String(100))  # Например, telegram_id, discord_id и т.д.
    identifier_type = Column(String(50))  # Тип идентификатора
    
    # Связь с пользователем
    user = relationship("User", back_populates="identifiers")

class Task(Base):
    """Основная модель задачи"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(200))
    progress = Column(Integer, default=0)  # Прогресс выполнения задачи (%)
    is_regular = Column(Boolean, default=False)  # Тип задачи: регулярная или нерегулярная
    
    # Связь с пользователем
    user = relationship("User", back_populates="tasks")
    
    # Связи с расширенными таблицами
    regular_task = relationship("RegularTask", back_populates="task", uselist=False, cascade="all, delete-orphan")
    irregular_task = relationship("IrregularTask", back_populates="task", uselist=False, cascade="all, delete-orphan")

class RegularTask(Base):
    """Модель регулярной задачи (расширение Task)"""
    __tablename__ = "regular_tasks"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    # Дни недели (строка в формате "1,2,3,4,5,6,7", где 1 - понедельник, 7 - воскресенье)
    weekdays = Column(String(20))
    
    # Связь с основной задачей
    task = relationship("Task", back_populates="regular_task")

class IrregularTask(Base):
    """Модель нерегулярной задачи (расширение Task)"""
    __tablename__ = "irregular_tasks"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    optimal_deadline = Column(Date)  # Оптимальный срок выполнения
    hard_deadline = Column(Date)     # Крайний срок выполнения
    
    # Связь с основной задачей
    task = relationship("Task", back_populates="irregular_task")