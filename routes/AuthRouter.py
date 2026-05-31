from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from utils.database import DB_DEPENDENCY
from utils.config import settings
from schemas.UserSchema import UserCreate, UserResponse
from schemas.TokenSchema import Token
from controllers import AuthController as auth_controller

from controllers.AuthController import get_current_user
from models.UserModel import User

router = APIRouter(
    prefix=settings.AUTH_PREFIX,
    tags=["Authentication"]
)

USER_DEPENDENCY = Annotated[User, Depends(get_current_user)]


@router.get("", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_all_users(db: DB_DEPENDENCY, current_user: USER_DEPENDENCY):
    return auth_controller.get_all_users(db)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(user_data: UserCreate, db: DB_DEPENDENCY):
    try:
        return auth_controller.create_user(db, user_data)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email or username already registered."
        )
        
@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DB_DEPENDENCY):
    user = auth_controller.login_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password."
        )
        
    token = auth_controller.create_access_token(user.username, user.id)
    return Token(access_token=token, token_type="bearer")