from passlib.context import CryptContext

from src.conf.config import config


class Auth:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    SECRET_KEY = config.SECRET_KEY
    ALGORITHM = 'HS256'

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

auth_service = Auth()
