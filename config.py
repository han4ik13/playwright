import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    EMAIL = os.getenv("USER_EMAIL")
    PASSWORD = os.getenv("USER_PASSWORD")
    SECRET_KEY = os.getenv("TWO_FA_SECRET")