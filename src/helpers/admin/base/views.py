from fastapi import Request
from sqladmin import ModelView

from helpers.admin.auth import check_accesses_level
from ..enums import AccessLevel


class CustomModelView(ModelView):
    def is_accessible(self, request: Request) -> bool:
        return check_accesses_level(
            AccessLevel.support, request.session["access_level"]
        )

    def is_visible(self, request: Request) -> bool:
        return check_accesses_level(
            AccessLevel.support, request.session["access_level"]
        )
