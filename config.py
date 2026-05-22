import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    EMAIL = os.getenv("USER_EMAIL")
    PASSWORD = os.getenv("USER_PASSWORD")
    SECRET_KEY = os.getenv("TWO_FA_SECRET")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    @classmethod
    def validate(cls):
        missing = [k for k, v in {
            "BASE_URL": cls.BASE_URL,
            "USER_EMAIL": cls.EMAIL,
            "USER_PASSWORD": cls.PASSWORD,
            "DB_HOST": cls.DB_HOST,
            "DB_NAME": cls.DB_NAME,
            "DB_USER": cls.DB_USER,
            "DB_PASSWORD": cls.DB_PASSWORD,
        }.items() if not v]
        if missing:
            raise EnvironmentError(f"Отсутствуют переменные окружения: {missing}")