from models.UserModel import User
from sqlalchemy.orm import Session

def get_all_users(db: Session):
    return db.query(User).all()