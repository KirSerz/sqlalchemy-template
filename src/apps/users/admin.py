from fastapi import Request

from db.models.user import User, UserSession
from helpers.admin.auth import check_accesses_level
from helpers.admin.base.views import CustomModelView
from helpers.admin.enums import AccessLevel


class UserAdmin(CustomModelView, model=User):
    column_exclude_list = ["sessions", "password"]
    column_details_exclude_list = ["sessions"]
    form_excluded_columns = ["sessions"]

    category = "users"

    async def on_model_change(self, data, model, is_created: bool):
        password = data.get("password")
        if password == "<PasswordHash>":
            data.pop("password")
        await super().on_model_change(data, model, is_created)

    def is_accessible(self, request: Request) -> bool:
        return check_accesses_level(
            AccessLevel.administrator, request.session["access_level"]
        )

    def is_visible(self, request: Request) -> bool:
        return check_accesses_level(
            AccessLevel.administrator, request.session["access_level"]
        )


class UserSessionAdmin(CustomModelView, model=UserSession):
    column_list = "__all__"
    category = "auth"

    def is_accessible(self, request: Request) -> bool:
        return check_accesses_level(
            AccessLevel.administrator, request.session["access_level"]
        )

    def is_visible(self, request: Request) -> bool:
        return check_accesses_level(
            AccessLevel.administrator, request.session["access_level"]
        )
