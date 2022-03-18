import os

# POSTGRES_CONFIG
DB_ENGINE = os.environ.get('DB_ENGINE', 'postgresql+asyncpg')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'todo_user')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'Or&Rlpt8')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'account_db')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'todo_account')
SQLALCHEMY_DATABASE_URL = (
    f"{DB_ENGINE}://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

# AUTH SECRETS
SECRET_KEY = os.environ.get("AUTH_SECRET", "SOME_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 60

# DEBUG
DEBUG = os.environ.get("DEBUG", True)