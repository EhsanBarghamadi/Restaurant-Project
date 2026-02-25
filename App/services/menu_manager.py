from app.models.menu import MenuItems
from app.database.database_manager import DatabaseManager

class MenuManager():
    """
    Docstring for MenuManager
    """
    def __init__(self, database_manager:DatabaseManager):
        self.db = database_manager

    def existence_item(self, name:str) -> tuple[bool, None | object]:
        name = name.title()
        query = """
                SELECT id, name, price, portions_left FROM menu_items
                WHERE name = %s
                """
        res, data = self.db.query_tool(query, params=(name,), fetch_one=True)
        if res:
            if data:
                menu_item = MenuItems(data[0], data[1], data[2], data[3])
                return True, menu_item
            return False, None
        return False, "Database error during insertion"
    
    def add_item(self, name:str, price:float, portions_left:int):
        name = name.title()
        result, obj = self.existence_item(name)
        if result:
            return False, f"There is a item {obj.name} in menu."
        query = """
                INSERT INTO menu_items(name, price, portions_left)
                VALUES (%s, %s, %s) RETURNING id
                """
        res, data = self.db.query_tool(query, params=(name, price, portions_left), fetch_one=True)
        if res and data:
            id_item = data[0]
            return True, f"{name} item added with ID {id_item}"
        return False, "Database error during insertion"
    
    def change_price(self, name:str, new_price:float) -> tuple[bool, str]:
        name = name.title()
        if new_price <= 0:
            return False, f"New price cannot be negative or zero."
        result, obj = self.existence_item(name)
        if not result:
            return False, f"There is not a item {name} in menu."
        query = """
                UPDATE menu_items
                SET price = %s
                WHERE id = %s
                """
        res, data = self.db.query_tool(query, params=(new_price, obj.id))
        if res:
            return True, f"{obj.name} item price changed from {obj.price} to {new_price}."
        return False, "Database error during insertion"
    
    def change_portions_left(self, name:str, new_portions_left:int) -> tuple[bool, str]:
        name = name.title()
        if new_portions_left < 0:
            return False, f"Prtions left cannot be negative or zero."
        result, obj = self.existence_item(name)
        if not result:
            return False, f"There is not a item {name} in menu."
        query = """
                UPDATE menu_items
                SET portions_left = %s
                WHERE id = %s
                """
        res, data = self.db.query_tool(query, params=(new_portions_left, obj.id))
        if res:
            return True, f"{obj.name} item portions left changed from {obj.portions_left} to {new_portions_left}."
        return False, "Database error during insertion"
      
    def delete_item(self, name:str) -> tuple[bool, str]:
        name = name.title()
        result, obj = self.existence_item(name)
        if not result:
            return False, f"There is not a item {name} in menu."
        query = """
                DELETE FROM menu_items
                WHERE id = %s
                """
        res, data = self.db.query_tool(query, params=(obj.id,))
        if res:
            return True, f"{obj.name} item was deleted."
        return False, "Database error during insertion"
    
    def get_all_items(self) -> tuple[bool, list[MenuItems] | str]:
        query = """
                SELECT id, name, price, portions_left 
                FROM menu_items ORDER BY name"""
        res, data = self.db.query_tool(query, fetch_all=True)
        if res:
            items = [MenuItems(row[0], row[1], row[2], row[3]) for row in data] if data else []
            return True, items
        return False, "Database error while fetching menu."