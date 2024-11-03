from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:

    @staticmethod
    def hash_password(password: str) -> str:
        return password_context.hash(password)

    @staticmethod
    def verify_password(hashed_password: str, plain_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)
