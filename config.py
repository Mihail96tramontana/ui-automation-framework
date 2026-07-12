import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
STANDARD_USER = os.getenv('STANDARD_USER')
LOCKED_USER = os.getenv('LOCKED_USER')
PASSWORD = os.getenv('PASSWORD')