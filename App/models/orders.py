from enum import Enum

class OrderStatus(Enum):
    RECEIVED = 'received'
    CANCELLED = 'cancelled'
    PREPARING = 'preparing'
    READY = 'ready'
    PAID = 'paid'

class Orders:
    def __init__(self, id: int, waiter, table, status: str, order_time=None, items=None):
        self.id = id
        self.waiter = waiter
        self.table = table
        self.status = OrderStatus(status)
        self.order_time = order_time
        self.items = items if items else list()

    def calculate_total_price(self):
        return sum(item.get_total_item_price() for item in self.items)
        