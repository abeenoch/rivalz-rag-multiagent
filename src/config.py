import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    RIVALZ_SECRET_TOKEN = os.getenv("RIVALZ_SECRET_TOKEN")
