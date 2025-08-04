import uuid

import bcrypt
from sqlalchemy import Column, ForeignKey, String, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import UUID, BigInteger, Enum, DateTime

from helpers.admin.enums import AccessLevel
from .base import Base
from ..types.fields import Password


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, unique=True, nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(Password(length=156), nullable=False)
    access_level = Column(Enum(AccessLevel))

    sessions = relationship("UserSession", back_populates="user")

    @validates("password")
    def _validate_password(self, key, password):
        return getattr(type(self), key).type.validator(password)

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password.hash.encode())


class UserSession(Base):
    __tablename__ = "user_sessions"

    token = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
        index=True,
        primary_key=True,
    )
    user_id = Column(BigInteger, ForeignKey("users.id"), index=True, nullable=False)

    user = relationship("User", back_populates="sessions")
    created_at = Column(DateTime, default=func.now(), nullable=False)

    @classmethod
    def _filter_session_by_user_id(cls, user_id: int):
        query = select(cls).where(cls.user_id == user_id)
        return query
