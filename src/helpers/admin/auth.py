from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from db import db_conn
from db.models.user import UserSession
from repositories.user_repository import UserRepository, UserSessionRepository
from .enums import AccessLevel


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        async with db_conn.async_session_manager() as session:
            user_rep = UserRepository(session)
            user = await user_rep.get_by_username(username=username)
            if user and user.verify_password(password):
                user_session_rep = UserSessionRepository(session)
                user_session = await user_session_rep.create(
                    UserSession(
                        user_id=user.id,
                    )
                )
                request.session.update(
                    {
                        "user_id": user_session.user_id,
                        "token": user_session.token.hex,
                        "access_level": user.access_level.value,
                    }
                )
                return True
            return False

    async def logout(self, request: Request) -> bool:
        async with db_conn.async_session_manager() as session:
            user_session_rep = UserSessionRepository(session)
            await user_session_rep.delete_by_token(request.session["token"])
            request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if token:
            async with db_conn.async_session_manager() as session:
                user_session_rep = UserSessionRepository(session)
                session = await user_session_rep.get_session_by_token(token)
                if session and session.user_id != request.session["user_id"]:
                    session = None
        else:
            session = None
        return bool(session)


def check_accesses_level(
    access_level: int | AccessLevel, user_access_level: int | AccessLevel
):
    if access_level > user_access_level:
        return False
    return True
