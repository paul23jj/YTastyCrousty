import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

admin_password = os.getenv("ADMIN_PASSWORD")

if admin_password:  