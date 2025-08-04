from pydantic import UUID4
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from db import User, UserSession
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_username(self, username: str):
        return await self.get(filters=[self.model.username == username])


class UserSessionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(UserSession, session)


    async def get_session_by_token(self, token: UUID4):
        return await self.get(filters=[self.model.token == token])

    async def delete_by_token(self, token: UUID4):
        query = delete(self.model).where(self.model.token == token)
        await self.session.execute(query)
        await self.session.commit()
