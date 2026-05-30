class Settings:
    DATABASE_URL: str = "sqlite:///./todosapp.db"
    
    PROJECT_TITLE: str = "Todo API"
    PROJECT_DESCRIPTION: str = "A Todo API using FastAPI and SQLAlchemy"
    PROJECT_VERSION: str = "1.0.0"
    
    TODO_PREFIX: str = "/todos"
    AUTH_PREFIX: str = "/auth"

settings = Settings()