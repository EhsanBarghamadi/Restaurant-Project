from app.models.user import Users, UserRoles
from app.models.orders import Orders, StatusOrder
from app.models.menu import MenuItems
from app.models.table import Table, TableStatus
from app.database.database_manager import DatabaseManager

db = DatabaseManager()

class Waiter(Users):
    """
    Subclass of Users for Waiter role, with methods for order management.
    """
    def __init__(self, id, username, password, roles=UserRoles.WAITER):
            super().__init__(id, username, password, roles)
            self.tables = list()
            if self.roles != UserRoles.WAITER:
                raise ValueError("This class is only for Waiter role.")

    def get_assigned_tables(self) -> list[Table]:
        self.tables = []
        query = """
                SELECT t.id, t.table_number, t.status FROM tables AS t
                INNER JOIN waiter_table
                ON t.id = waiter_table.table_id
                WHERE waiter_table.user_id = %s
                """
        result, fetch = db.query_tool(query, params=(self.id,) ,fetch=True)
        if result:
            list_assigned = [Table(item[0], item[1], item[2]) for item in fetch]
            self.tables = list_assigned
            return self.tables
        return []
    
    def create_order(self, table: Table) -> Orders:
        if table.status.value == TableStatus.OCCUPIED:
            raise Exception("Table is not available.")
        self.get_assigned_tables()
        if any(t.id == table.id for t in self.tables):
            order = Orders(None, self, table)
            order.save()
            table.status = TableStatus.OCCUPIED
            table.save()
            return order

    def add_item_to_order(self, order: Orders, menu_item: MenuItems, quantity: int):
        if order.user.id != self.id:
            raise Exception("Not your order.")        
        order.add_item(menu_item, quantity)

    def remove_item_from_order(self, order: Orders, menu_item: MenuItems):
        if order.user.id != self.id:
            raise Exception("Not your order.")        
        order.remove_item(menu_item)

    def update_order_status(self, order: Orders, new_status: str):
        if order.user.id != self.id:
            raise Exception("Not your order.")
        order.update_status(new_status)