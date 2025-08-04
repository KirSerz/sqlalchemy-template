import argparse
import asyncio

from db import db_conn
from db.models.user import User
from helpers.logging import logger
from repositories.user_repository import UserRepository


parser = argparse.ArgumentParser()
parser.add_argument("-un", "--username", help="user name", required=True)
parser.add_argument(
    "-al", "--access_level", type=int, help="access level", required=False
)
parser.add_argument("-pass", "--password", type=str, help="password", required=True)

args = parser.parse_args()


async def main():
    username = args.username
    async with db_conn.async_session_manager() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_username(username)
        if user:
            await user_repo.update(
                user.id, password=args.password.encode(), access_level=args.access_level
            )
            logger.info(f"User {username} updated! access_level: {args.access_level}")
        else:
            await user_repo.create(
                User(
                    password=args.password,
                    access_level=args.access_level,
                    username=username,
                )
            )
            logger.info(f"User {username} created! access_level: {args.access_level}")


if __name__ == "__main__":
    asyncio.run(main())
