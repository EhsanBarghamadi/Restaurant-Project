from app.database.database_manager import DatabaseManager
from app.models.user import Users
from app.models.table import Table
from app.models.menu import MenuItems
from app.models.orderitems import OrderItem
from enum import Enum
db = DatabaseManager()

class StatusOrder(Enum):
    RECEIVED = 'received'
    CANCELLED = 'cancelled'
    PREPARING = 'preparing'
    READY = 'ready'
    PAID = 'paid'

class Orders():
    '''
    Docstring for Orders
    '''
    def __init__(self, id, user: Users, table: Table, status: StatusOrder='received', order_items=None):
        self.id = id
        self.user = user
        self.table = table
        self.status = StatusOrder(status)
        self.order_items = order_items or list()

    def save(self) -> tuple[bool, str]:
        if self.id:
            query = """
                    UPDATE orders
                    SET waiter_id = %s, table_id = %s, status = %s 
                    WHERE id = %s
                    """
            result, outcome = db.query_tool(query, params=(self.user.id, self.table.id, self.status.value, self.id))
        else: 
            query = """
                    INSERT INTO orders (waiter_id, table_id, status) 
                    VALUES (%s, %s, %s) RETURNING id
                    """
            result, outcome = db.query_tool(query, params=(self.user.id, self.table.id, self.status.value), fetch=True)
            if result:
                outcome = outcome[0][0]
                self.id = outcome
        if result and self.order_items:
            for item in self.order_items:
                item.save(self.id)
        return result, outcome
    
    def remove_item(self, menu_item: MenuItems) -> OrderItem | None:
        for item in self.order_items:
            if item.menu_item.id == menu_item.id:                
                self.order_items.remove(item)
                return item.remove()
            
    def add_item(self, menu_item:MenuItems, quantity:int) -> tuple[bool, str]:
        for item in self.order_items:
            if item.menu_item.id == menu_item.id:
                item.quantity += quantity
                item.save(self.id)
                return True, f"The quantity of {item.menu_item.name} has increased."
        new_item = OrderItem(menu_item, quantity)
        self.order_items.append(new_item)
        new_item.save(self.id)
        self.save()
        return True, "The desired item has been added to the order."
    
    def calculate_total(self) -> int:
        if not self.order_items:
            return 0
        all_total = 0
        for item in self.order_items:
            all_total += item.menu_item.price * item.quantity
        return all_total
    
    def update_status(self, new_status:str):
        self.status = StatusOrder(new_status.lower())
        self.save()
        return True