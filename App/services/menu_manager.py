from app.models.menu import MenuItems
from app.database.database_manager import DatabaseManager
from datetime import datetime

db = DatabaseManager()

class MenuManager():
    """
    Docstring for MenuManager
    """
    def __init__(self):
        self.all_items = list()

    def existence_item(self, name):
        name = name.capitalize()
        select_item = [item for item in self.all_items if item.name == name]
        if select_item:
            return True, select_item[0]
        return False, None
    
    def add_item(self, name, price, portions_left):
        result, obj = self.existence_item(name)
        if result:
            return False, f"There is a item {obj.name} in menu."
        query = "INSERT INTO menu_items(name, price, portions_left) VALUES (%s, %s, %s) RETURNING id"
        result, id = db.query_tool(query, (name, price, portions_left), True)
        if not result:
            return False, f"Error Database: {id}"
        self.all_items.append(MenuItems(id[0][0], name.capitalize(), price, portions_left))
        return True, f"Item Menu {name} added successfully."
    
    def load_all(self):
        query = "SELECT id, name, price, portions_left FROM menu_items"
        result, fetch = db.query_tool(query, fetch=True)
        if result:
            for item in fetch:
                self.all_items.append(MenuItems(item[0], item[1], item[2], item[3]))
        return datetime.now()
    
    def change_price(self, name, new_price):
        result, obj = self.existence_item(name)
        if not result:
            return False, f"Item {name} does not exist. Please add it first."
        obj.price = new_price
        obj.save()

    def change_portions_left(self, name, new_portions_left):
        result, obj = self.existence_item(name)
        if not result:
            return False, f"Item {name} does not exist. Please add it first."
        obj.portions_left = new_portions_left
        obj.save()