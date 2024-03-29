from datetime import datetime
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy import select, update


from database.models import Order, OrderItem, Product, User
from database.connection import async_session


class OrderService:
    async def create_order(order, order_items):
        async with async_session() as session:
            existing_user = await session.execute(select(User).where(User.id == order.user_id))
            user = existing_user.scalar()

            if user is None:
                raise ValueError("User does not exist")
            total = order.shipping_cost + \
                sum([item.price * item.quantity for item in order_items])
            new_order = Order(
                user_id=order.user_id,
                # payment_pending, processing, in_transit, cancelled, delivered, returned, payment_failed, refunded
                status=order.status,
                total_amount=total,
                shipping_cost=order.shipping_cost,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            session.add(new_order)
            await session.flush()

            for item in order_items:
                existing_product = await session.execute(select(Product).where(Product.id == item.product_id))
                product = existing_product.scalar()

                if product is None:
                    raise ValueError(
                        f"Product with id {item.product_id} does not exist")

                if product.stock_quantity < item.quantity:
                    raise ValueError(
                        f"Product with id {item.product_id} does not have enough stock")

                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )

                session.add(order_item)

                await session.execute(
                    update(Product).where(Product.id == product.id).values(
                        updated_at=datetime.now(),
                        stock_quantity=Product.stock_quantity - item.quantity
                    )
                )

            await session.commit()

    async def get_order(order_id):
        async with async_session() as session:
            query = select(Order).where(Order.id == order_id)
            db_order = await session.execute(query)

            order = db_order.fetchone()
            if not order:
                raise ValueError("Order does not exist")

            order_itens = await session.execute(select(OrderItem).where(OrderItem.order_id == order_id))
            order_itens = order_itens.fetchall()
            order_itens_data = [order_item._asdict()
                                for order_item in order_itens]
            order_data = order._asdict()
            order_data["order_itens"] = order_itens_data
            if order_itens:
                product_ids = [order_item.product_id for order_item in order_itens_data]
                products = await session.execute(select(Product).where(Product.id.in_(product_ids)))
                products = products.fetchall()
                products_data = [product._asdict() for product in products]
                order_data["products"] = products_data

            return order_data

    async def get_orders():
        async with async_session() as session:
            query = select(Order)
            db_orders = await session.execute(query)

            orders = db_orders.fetchall()
            if not orders:
                raise ValueError("Order does not exist")
            orders_data = [order._asdict() for order in orders]
            return orders_data

    async def update_order(order_id, order):
        async with async_session() as session:
            query_order = select(Order).where(Order.id == order_id)
            db_order = await session.execute(query_order)
            order = db_order.scalar()
            if not order:
                raise ValueError("Order does not exist")
            query_order_items = select(OrderItem).where(OrderItem.order_id == order_id)
            db_order_items = await session.execute(query_order_items)
            order_items = db_order_items.fetchall()
            if not order_items:
                total = 0
            else:
                total = order.shipping_cost + \
                    sum([item.price * item.quantity for item in order_items])
                    
            await session.execute(
                update(Order).where(Order.id == order_id).values(
                    status=order.status,
                    total_amount=total,
                    shipping_cost=order.shipping_cost,
                    updated_at=datetime.now()
                )
            )

            for item in order.order_items:
                query = select(OrderItem).where(
                    OrderItem.id == item.id, OrderItem.product_id == item.product_id)
                db_order_item = await session.execute(query)

                if db_order_item.scalar():
                    await session.execute(
                        update(OrderItem).where(OrderItem.id == item.id).values(
                            quantity=item.quantity,
                            price=item.price,
                            updated_at=datetime.now()
                        )
                    )
                else:
                    new_item = OrderItem(
                        order_id=order_id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                    )
                    await session.add(new_item)

            await session.commit()

    async def get_orders_by_user(user_id):
        async with async_session() as session:
            query = select(Order).where(Order.user_id == user_id)
            db_orders = await session.execute(query)

            orders = db_orders.fetchall()
            if not orders:
                raise ValueError("There are no orders")
            orders_data = [order._asdict() for order in orders]
            return orders_data

    async def get_orders_by_status(status):
        async with async_session() as session:
            query = select(Order).where(Order.status == status)
            db_orders = await session.execute(query)

            orders = db_orders.fetchall()
            if not orders:
                raise ValueError("Orders does not exist")
            orders_data = [order._asdict() for order in orders]
            return orders_data

    async def get_orders_by_user_and_status(user_id, status):
        async with async_session() as session:
            query = select(Order).where(Order.user_id ==
                                        user_id).where(Order.status == status)
            db_orders = await session.execute(query)

            orders = db_orders.fetchall()
            if not orders:
                raise ValueError("Orders does not exist")
            orders_data = [order._asdict() for order in orders]
            return orders_data
