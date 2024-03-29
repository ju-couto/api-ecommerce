from datetime import datetime
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy import select, update


from database.models import Category, Product
from database.connection import async_session


class CategoryService:
    async def create_category(category):
        async with async_session() as session:
            category_query = select(Category).where(
                Category.name == category.name)
            db_category = await session.execute(category_query)
            existing_category = db_category.fetchone()

            if existing_category is not None:
                raise ValueError("Category already exists")

            new_category = Category(
                name=category.name,
                created_at=datetime.now(),
                updated_at=datetime.now(),

            )

            session.add(new_category)
            await session.commit()

    async def get_category(category_id):
        async with async_session() as session:
            query = select(Category).where(Category.id == category_id)
            db_category = await session.execute(query)

            existing_category = db_category.fetchone()
            if not existing_category:
                raise ValueError("Category does not exist")
            category_data = existing_category._asdict()
            return category_data

    async def get_categories():
        async with async_session() as session:
            query = select(Category).where(Category.active == True)
            db_categories = await session.execute(query)

            categories = db_categories.fetchall()
            if not categories:
                raise ValueError("Category does not exist")
            categories_data = [category._asdict() for category in categories]
            return categories_data

    async def delete_category(category_id):
        async with async_session() as session:
            category_query = select(Category).where(Category.id == category_id)
            db_category = await session.execute(category_query)
            category = db_category.scalar()
            products_query = select(Product).where(
                Product.category_id == category_id)
            db_products = await session.execute(products_query)
            products = db_products.fetchall()
            if products:
                raise ValueError("Category has products")

            if not category:
                raise ValueError("Category does not exist")

            if category.active == False:
                raise ValueError("Category already deleted")

            await session.execute(update(Category).where(Category.id == category_id).values(
                active=False,
                updated_at=datetime.now()
            ))
            await session.commit()

    async def update_category(category_id, category):
        async with async_session() as session:
            query = select(Category).where(Category.id == category_id)
            db_category = await session.execute(query)

            if not db_category.scalar():
                raise ValueError("Category does not exist")

            await session.execute(
                update(Category).where(Category.id == category_id).values(
                    name=category.name,
                    updated_at=datetime.now()
                )
            )
            await session.commit()
