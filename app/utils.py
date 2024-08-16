from passlib.context import CryptContext # cryptography


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hashing password
def hash(password: str):
    return pwd_context.hash(password)