from app.models.orders import Orders, OrderStatus
from app.models.order_items import OrderItem
from app.services.menu_manager import MenuManager
from app.services.table_manager import TableManager
from app.services.user_manager import UserManager
from app.database.database_manager import DatabaseManager

class OrderManager():
    ''' 
    Docstring for OrderManager
    '''
    def __init__(self, database_manager : DatabaseManager, user_manager: UserManager, menu_manager : MenuManager, table_manager: TableManager):
        self.db = database_manager
        self.mu_manager = menu_manager
        self.ta_manager = table_manager
        self.us_manager = user_manager

    def existence_order(self, order_id:int) -> tuple[bool , Orders | str]:
        query = """
                SELECT users.username, tables.table_number, orders.status, orders.order_time
                FROM orders
                INNER JOIN tables
                ON orders.table_id = tables.id
                INNER JOIN users
                ON orders.waiter_id = users.id
                WHERE orders.id = %s
                """
        re, data = self.db.query_tool(query, params=(order_id,), fetch_one=True)
        if re:
            if data:
                    username, table_number, orders_status, order_time = data
                    res, user_obj = self.us_manager.existence_user(username)
                    resu, table_obj = self.ta_manager.existence_table(table_number)
                    query = """
                            SELECT order_details.id, menu_items.name, order_details.quantity
                            FROM orders
                            INNER JOIN order_details
                            ON orders.id = order_details.order_id
                            INNER JOIN menu_items
                            ON order_details.menu_item_id = menu_items.id
                            WHERE order_details.order_id = %s
                            """
                    resul, info = self.db.query_tool(query, params=(order_id,), fetch_all=True)
                    if res and resu and resul:
                        items_list = list()
                        if not any(None in item for item in info):
                            for details_id, menu_name, quantity in info:
                                result, item_obj = self.mu_manager.existence_item(menu_name)
                                if result:
                                    new_orderitem = OrderItem(item_obj, quantity, details_id)
                                    items_list.append(new_orderitem)
                            order_obj = Orders(order_id, user_obj, table_obj, orders_status, order_time, items_list)
                            return True, order_obj
                        order_obj = Orders(order_id, user_obj, table_obj, orders_status, order_time)
                        return True, order_obj
                    if not res or not resu:
                        return False, "Waiter or Table information is inconsistent in the database."
            return False, "The requested order ID was not found."
        return False, "Database error during insertion"
    
    def add_order(self, username: str, table_number: int) -> tuple[bool, Orders | str]:
        re, witer_obj = self.us_manager.existence_user(username)
        res, table_obj = self.ta_manager.existence_table(table_number)
        if not re or witer_obj is None:
            return False, f"Waiter '{username}' not found."
        if not res or table_obj is None:
            return False, f"Table number {table_number} not found."
        if table_obj.status.value != "available":
            return False, f"Table number {table_number} is already occupied."
        query = """
                INSERT INTO orders (waiter_id, table_id, status)
                VALUES
                (%s, %s, 'received')
                RETURNING id, order_time
                """
        resu, data = self.db.query_tool(query, params=(witer_obj.id, table_obj.id), fetch_one=True)
        if resu:
            order_id, order_time= data
            order_obj = Orders(order_id, witer_obj, table_obj,'received', order_time)
            return True, order_obj
        return False, "Database error during insertion"
    
    def add_item_to_order(self, order_obj: Orders, item_name: str, quantity: int) -> tuple[bool, str]:
        re, item_obj = self.mu_manager.existence_item(item_name)
        if not re or item_obj is None:
            return False, f"{item_name} item not found"
        if item_obj.portions_left < quantity:
            return False, f"The desired item is not available in quantity {quantity}."
        query = """
                INSERT INTO  order_details (order_id, menu_item_id, quantity)
                VALUES
                (%s, %s, %s)
                RETURNING id
                """
        res, data = self.db.query_tool(query, params=(order_obj.id, item_obj.id, quantity), fetch_one=True)
        if res:
            order_item_id = data[0]
            order_item_obj = OrderItem(item_obj, quantity, order_item_id)
            order_obj.items.append(order_item_obj)
            return True, f"Added {quantity}x {item_obj.name} to order #{order_obj.id}."
        return False, "Database error during insertion"

    def update_order_status(self, order_obj: Orders, new_status: OrderStatus) -> tuple[bool, str]:
        query = """
                UPDATE orders 
                SET status = %s 
                WHERE id = %s
                """
        res, msg = self.db.query_tool(query, params=(new_status.value, order_obj.id))
        if res:
            order_obj.status = new_status
            return True, f"Order #{order_obj.id} status updated to {new_status.value}."
        return False, "Database error during status update."  
        
    def remove_item_from_order(self, order_obj: Orders, item_name: str) -> tuple[bool, str]:
        find_item = [order_item for order_item in order_obj.items if order_item.menu_item.name == item_name]
        if not find_item:
            return False, f"{item_name} item not found in order ID {order_obj.id}"
        order_item_obj = find_item[0]
        query = """
                DELETE FROM order_details
                WHERE id = %s
                """
        res, info = self.db.query_tool(query, params=(order_item_obj.id,))
        if res:
            order_obj.items.remove(order_item_obj)
            return True, f"Item {item_name} removed from order."
        return False, "Database error during item deletion."
    
    def update_item_quantity(self, order_obj: Orders, item_name: str, new_quantity: int) -> tuple[bool, str]:
        find_item = [order_item for order_item in order_obj.items if order_item.menu_item.name == item_name]
        if not find_item:
            return False, f"{item_name} item not found in order ID {order_obj.id}"
        order_item_obj = find_item[0]
        if (order_item_obj.menu_item.portions_left + order_item_obj.quantity) < new_quantity:
            return False, f"The desired item is not available in quantity {new_quantity}."
        query = """
                UPDATE order_details 
                SET quantity = %s 
                WHERE id = %s
                """
        re, info = self.db.query_tool(query, params=(new_quantity, order_item_obj.id))
        if re:
            old_quantity = order_item_obj.quantity
            order_item_obj.quantity = new_quantity
            return True, f"{order_item_obj.menu_item.name} items required changed from {old_quantity} to {new_quantity}."
        
    def get_waiter_orders(self, username: str) -> tuple[bool, list[Orders] | str]:
        re, waiter_obj = self.us_manager.existence_user(username)
        if not re or waiter_obj is None:
            return False, f"Waiter '{username}' not found."
        query = """
                SELECT id FROM orders
                WHERE waiter_id = %s
                AND DATE(order_time) = CURRENT_DATE
                ORDER BY status DESC
                """
        res, data = self.db.query_tool(query, params=(waiter_obj.id,), fetch_all=True)
        if res:
            if not data:
                return True, []
            order_list = list()
            for (order_id,) in data:
                resu, order_obj = self.existence_order(order_id)
                if not resu:
                    return False, order_obj
                order_list.append(order_obj)
            return True, order_list

    def get_invoice(self, order_obj: Orders) -> str:
        return order_obj.calculate_total_price()

            