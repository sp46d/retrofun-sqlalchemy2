import sqlalchemy as sa
from retrofun.models import Order, OrderItem, Customer, Product


def total_orders(search: str):
    if not search:
        return sa.select(sa.func.count(Order.id))
    
    return (
        sa.select(sa.func.count(sa.distinct(Order.id)))
            .join(Order.customer)
            .join(Order.order_items)
            .join(OrderItem.product)
            .where(sa.or_(Customer.name.ilike(f'%{search}%'),
                          Product.name.ilike(f'%{search}%')))
            
    )


def paginated_orders(start: int, 
                     length: int, 
                     sort: str,
                     search: str):
    """
    returns a list of orders
    """
    total = sa.func.sum(OrderItem.unit_price * OrderItem.quantity).label(None)
    q = (sa.select(Order, total)
         .join(Order.customer)
         .join(Order.order_items)
         .join(OrderItem.product)
         .group_by(Order))
    
    if search:
        q = q.where(
            sa.or_(Customer.name.like(f'%{search}%'),
                   Product.name.like(f'%{search}%'))
        )

    if sort:
        order = []
        for s in sort.split(','):
            s = s.strip()
            direction = s[0]
            name = s[1:]
            if name == 'customer':
                column = Customer.name
            elif name == 'total':
                column = total
            else:
                column = getattr(Order, name)
            if direction == '-':
                column = column.desc()
            order.append(column)
            
        if not order:
            order = [Order.timestamp.desc()]
            
        q = q.order_by(*order)
        
    q = q.offset(start).limit(length)
    
    return q