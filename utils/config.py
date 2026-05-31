import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = "sqlite:///./todosapp.db"
    

    PROJECT_TITLE: str = "Todo API"
    PROJECT_DESCRIPTION: str = "A Todo API using FastAPI and SQLAlchemy"
    PROJECT_VERSION: str = "1.0.0"
    

    TODO_PREFIX: str = "/todos"
    AUTH_PREFIX: str = "/auth"
    

    SECRET_KEY: str = os.getenv("SECRET_KEY", "SampleSecretKeyForJWT")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

settings = Settings()