from datetime import datetime
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy import delete, select, update


from database.models import Product, Category
from database.connection import async_session


class ProductService:
    async def create_product(product):
        async with async_session() as session:
            category_query = select(Category).where(Category.id == product.category_id)
            db_category = await session.execute(category_query)
            existing_category = db_category.fetchone()
            
            if existing_category is None:
                raise ValueError("Category does not exist")
            
            
            product_query = select(Product).where(Product.name == product.name)
            db_products = await session.execute(product_query)
            existing_product = db_products.fetchone()
            
            if existing_product is not None:
                raise ValueError("Product already exists")


            new_product = Product(
                name=product.name,
                price=product.price,
                description=product.description,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                stock_quantity=product.stock_quantity,
                category_id=product.category_id,
                image_url=product.image_url
                
            )
                

            session.add(new_product)
            await session.commit()

    async def get_product(product_id):
        async with async_session() as session:
            query = select(Product).where(Product.id == product_id)
            db_product = await session.execute(query)

            product = db_product.fetchone()
            if not product:
                raise ValueError("Product does not exist")
            product_data = product._asdict()
            return product_data

    async def get_products():
        async with async_session() as session:
            query = select(Product)
            db_products = await session.execute(query)

            products = db_products.fetchall()
            if not products:
                raise ValueError("Product does not exist")
            products_data = [product._asdict() for product in products]
            return products_data

    async def get_products_by_category(category_id):
        async with async_session() as session:
            query = select(Product).where(Product.category_id == category_id)
            db_products = await session.execute(query)

            products = db_products.fetchall()
            if not products:
                raise ValueError("Products of this category does not exist")
            products_data = [product._asdict() for product in products]
            return products_data
        
        
    async def delete_product(product_id):
        async with async_session() as session:
            query = select(Product).where(Product.id == product_id)
            db_product = await session.execute(query)

            if not db_product.scalar():
                raise ValueError("Product does not exist")

            await session.execute(delete(Product).where(Product.id == product_id))
            await session.commit()

    async def update_product(product_id, product):
        async with async_session() as session:
            query = select(Product).where(Product.id == product_id)
            db_product = await session.execute(query)

            if not db_product.scalar():
                raise ValueError("Product does not exist")

            query_name = select(Product).where(Product.name == product.name)
            db_product_name = await session.execute(query_name)
            existing_product = db_product_name.scalar()

            if existing_product is not None and existing_product.id != product_id:
                raise ValueError("Product already exists")

            await session.execute(
                update(Product).where(Product.id == product_id).values(
                    name=product.name,
                    price=product.price,
                    description=product.description,
                    updated_at=datetime.now(),
                    stock_quantity=product.stock_quantity,
                    category_id=product.category_id,
                    image_url=product.image_url
                )
            )
            await session.commit()
