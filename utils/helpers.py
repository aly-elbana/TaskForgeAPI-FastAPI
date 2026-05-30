from passlib.context import CryptContext

hashing_function = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return hashing_function.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashing_function.verify(plain_password, hashed_password)