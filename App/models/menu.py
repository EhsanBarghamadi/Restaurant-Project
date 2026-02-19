from app.database.database_manager import DatabaseManager

db = DatabaseManager()

class MenuItems():
    """
    Docstring for MenuItems
    """
    def __init__(self, id, name, price, portions_left):
        self.id = id
        self.name = name 
        self.price = price 
        self.portions_left = portions_left

    def save(self):
        query = "UPDATE menu_items SET price = %s, portions_left = %s WHERE id = %s"
        result, text = db.query_tool(query, params=(self.price, self.portions_left, self.id))
        return result, text