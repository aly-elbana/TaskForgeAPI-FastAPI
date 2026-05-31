from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError

from utils.database import DB_DEPENDENCY
from utils.config import settings
from utils.helpers import get_password_hash, verify_password
from models.UserModel import User
from schemas.UserSchema import UserCreate
from schemas.TokenSchema import TokenData

oauth2_bearer = OAuth2PasswordBearer(tokenUrl=f"{settings.AUTH_PREFIX.strip('/')}/login")

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user_data: UserCreate):
    user_dict = user_data.model_dump()
    
    plain_password = user_dict.pop("password") 
    user_dict["hashed_password"] = get_password_hash(plain_password)
    
    new_user = User(**user_dict)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def login_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not verify_password(password, user.hashed_password):
        return None
        
    return user

def create_access_token(username: str, user_id: int):
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_time = datetime.now(timezone.utc) + expires_delta
    
    to_encode = {
        "sub": username, 
        "user_id": user_id, 
        "exp": expire_time
    }
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)], 
    db: DB_DEPENDENCY
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username)
        
    except InvalidTokenError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    
    if user is None:
        raise credentials_exception
        
    return user