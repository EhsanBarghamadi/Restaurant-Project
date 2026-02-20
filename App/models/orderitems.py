from app.models.menu import MenuItems
from app.database.database_manager import DatabaseManager

db = DatabaseManager()

class OrderItem:
    def __init__(self, menu_item: MenuItems, quantity: int, id=None):
        self.id = id
        self.menu_item = menu_item
        self.quantity = quantity
        
    def save(self, order_id):
        if self.id:
            query = "UPDATE order_details SET quantity = %s WHERE id = %s"
            return db.query_tool(query, (self.quantity, self.id))
        else:
            query = "INSERT INTO order_details (order_id, menu_item_id, quantity) VALUES (%s, %s, %s) RETURNING id"
            result, new_id = db.query_tool(query, (order_id, self.menu_item.id, self.quantity), fetch=True)
            if result:
                self.id = new_id[0][0]
            return result, new_id
        
    def remove(self):
        if self.id:
            query = "DELETE FROM order_details WHERE id = %s"
            return db.query_tool(query, (self.id,))
        else:
            return None