from typing import Any

from fastapi import FastAPI
from sqladmin.application import Admin

from apps.users.admin import UserAdmin, UserSessionAdmin
from core.env import ADMIN_SECRET_KEY
from helpers.admin.auth import AdminAuth


def init(app: FastAPI, engine: Any):
    """
    Init routers and etc.
    :return:
    """
    init_admin(app, engine)
    init_routers(app)


def init_routers(app: FastAPI):
    """
    Initialize routers defined in `app.api`
    :param app:
    :return:
    """
    pass


def init_admin(app: FastAPI, engine: Any):
    authentication_backend = AdminAuth(secret_key=ADMIN_SECRET_KEY)
    admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(UserSessionAdmin)
