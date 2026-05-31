from fastapi import FastAPI, status
from utils.database import engine, Base
from routes import TodoRouter as todo_routes
from routes import AuthRouter as auth_routes
from utils.config import settings


app = FastAPI(
    title=settings.PROJECT_TITLE,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION
)

Base.metadata.create_all(bind=engine)

app.include_router(todo_routes.router)
app.include_router(auth_routes.router)

@app.get("/", tags=["Root"], status_code=status.HTTP_200_OK)
async def health_check() -> dict:
    return {"status": "Healthy", "message": "Welcome to the Clean Architecture API"}