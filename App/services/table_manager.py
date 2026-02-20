from app.models.table import TableStatus,Table
from app.database.database_manager import DatabaseManager
from datetime import datetime

db = DatabaseManager()

class TableManager():
    '''
    Docstring for TableManager
    '''
    def __init__(self):
        self.all_table = list()
        self.load = self.load_all()

    def existence_table(self, table_number:int) -> tuple[bool, None | object]:
        table_numbers = [table for table in self.all_table if table.table_number == table_number]
        if table_numbers:
            return True, table_numbers[0]
        return False, None

    def add_table(self, table_number:int) -> tuple[bool, str]:
        result, obj = self.existence_table(table_number)
        if result:
            return False, f"There is a table {obj.table_number}."
        query = "INSERT INTO tables(table_number) VALUES (%s) RETURNING id"
        result, id = db.query_tool(query, (table_number,), True)
        if not result:
            return False, f"Error Database: {id}"
        self.all_table.append(Table(id[0][0], table_number, TableStatus('available')))
        return True, f"Table {table_number} added successfully."

    def load_all(self) -> datetime:
        self.all_items = []
        query = "SELECT id, table_number, status FROM tables"
        result, fetch = db.query_tool(query, fetch=True)
        if result:
            for item in fetch:
                self.all_table.append(Table(item[0], item[1], TableStatus(item[2])))
        return datetime.now()
    
    def reserve_table(self, table_number:int):
            result, table = self.existence_table(table_number)
            if result and table.status == TableStatus.AVAILABLE:
                table.status = TableStatus.OCCUPIED
                table.save()
                return True, f"Table {table_number} is now occupied."
            return False, "Table is already occupied or does not exist."