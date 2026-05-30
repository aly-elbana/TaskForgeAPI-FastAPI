from fastapi import APIRouter, status
from controllers import AuthController as auth_controller
from utils.database import DB_DEPENDENCY

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_todos(db: DB_DEPENDENCY):
    return auth_controller.get_all_users(db)