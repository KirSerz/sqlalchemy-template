import os


POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_NAME = os.environ.get('POSTGRES_NAME', 'postgres')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv(
    "LOG_FORMAT", "[%(levelname)s]: %(message)s | %(pathname)s:%(funcName)s:%(lineno)d"
)

ADMIN_SECRET_KEY = os.environ.get("ADMIN_SECRET_KEY")
