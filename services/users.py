from datetime import datetime
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy import select, update
import bcrypt

from database.models import User
from database.connection import async_session


class UserService:
    async def create_user(user):
        async with async_session() as session:
            query = select(User).where(User.email == user.email)
            db_user = await session.execute(query)

            existing_user = db_user.fetchone()
            if existing_user is not None:
                raise ValueError("User already exists")

            hashed_password = bcrypt.hashpw(
                user.password.encode(), bcrypt.gensalt())
            hashed_password_str = hashed_password.decode('utf-8')

            new_user = User(
                name=user.name,
                email=user.email,
                password=hashed_password_str,
                address=user.address,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            session.add(new_user)
            await session.commit()

    async def get_user(user_id):
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            db_user = await session.execute(query)

            user = db_user.fetchone()
            if not user:
                raise ValueError("User does not exist")
            user_data = user._asdict()
            return user_data

    async def get_users():
        async with async_session() as session:
            query = select(User).where(User.active == True)
            db_users = await session.execute(query)

            users = db_users.fetchall()
            if not users:
                raise ValueError("There are no users")
            users_data = [user._asdict() for user in users]
            return users_data

    async def delete_user(user_id):
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            db_user = await session.execute(query)
            user = db_user.scalar()

            if not user:
                raise ValueError("User does not exist")

            if user.active == False:
                raise ValueError("User already deleted")

            await session.execute(update(User).where(User.id == user_id).values(
                active=False,
                updated_at=datetime.now()
            ))
            await session.commit()

    async def update_user(user_id, user):
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            db_user = await session.execute(query)

            if not db_user.scalar():
                raise ValueError("User does not exist")

            query_email = select(User).where(User.email == user.email)
            db_user_email = await session.execute(query_email)
            existing_user = db_user_email.scalar()

            if existing_user is not None and existing_user.id != user_id:
                raise ValueError("Email already exists")

            await session.execute(
                update(User).where(User.id == user_id).values(
                    name=user.name,
                    email=user.email,
                    address=user.address,
                    updated_at=datetime.now()
                )
            )
            await session.commit()
