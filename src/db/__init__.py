from core.db_config import db_settings
from .models.user import *
from .providers import DataAsyncProvider


db_conn = DataAsyncProvider(db_settings.db_url)
