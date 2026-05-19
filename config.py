import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    EMAIL = os.getenv("USER_EMAIL")
    PASSWORD = os.getenv("USER_PASSWORD")
    SECRET_KEY = os.getenv("TWO_FA_SECRET")

    @classmethod
    def validate(cls):
        missing = [k for k, v in {
            "BASE_URL": cls.BASE_URL,
            "USER_EMAIL": cls.EMAIL,
            "USER_PASSWORD": cls.PASSWORD,
        }.items() if not v]
        if missing:
            raise EnvironmentError(f"Отсутствуют переменные окружения: {missing}")