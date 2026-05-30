from sqlalchemy.orm import Session
from models.UserModel import User
from schemas.UserSchema import UserCreate
from utils.helpers import get_password_hash, verify_password

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user_data: UserCreate):
    user_dict = user_data.model_dump()
    plain_password = user_dict.pop("password") 
    hashed_password = get_password_hash(plain_password)
    user_dict["hashed_password"] = hashed_password
    
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
