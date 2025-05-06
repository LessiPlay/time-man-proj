from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class Database:
    """Класс для работы с базой данных"""
    
    def __init__(self, db_url):
        """
        Инициализация подключения к базе данных
        
        Args:
            db_url (str): URL для подключения к базе данных
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Создание всех таблиц в базе данных"""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """
        Получение сессии для работы с базой данных
        
        Returns:
            Session: Сессия SQLAlchemy
        """
        return self.Session()