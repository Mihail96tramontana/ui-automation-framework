import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
STANDARD_USER = os.getenv('STANDARD_USER')
LOCKED_USER = os.getenv('LOCKED_USER')
PASSWORD = os.getenv('PASSWORD')
NAME = os.getenv('FIRST_NAME')
LAST_NAME = os.getenv('LAST_NAME')
POSTAL_CODE = os.getenv('POSTAL_CODE')