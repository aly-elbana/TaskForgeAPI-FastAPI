from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt

from models.UserModel import User
from schemas.UserSchema import UserCreate
from utils.helpers import get_password_hash, verify_password
from utils.config import settings

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