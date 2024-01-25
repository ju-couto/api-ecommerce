from datetime import datetime
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy import delete, select
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
            
            hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
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
    
    async def is_admin(user_id):
        async with async_session() as session:
            db_user = select(User).where(User.id == user_id)
            if not db_user:
                raise ValueError("User does not exist")
            
            return db_user.role == "admin"
            
    async def delete_user(user_id):
        async with async_session() as session:
            query = select(User).where(User.id == user_id)
            db_user = await session.execute(query)
            
            if not db_user.scalar():
                raise ValueError("User does not exist")
             
            await session.execute(delete(User).where(User.id==user_id))
            await session.commit()