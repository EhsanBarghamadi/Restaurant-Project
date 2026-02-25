from app.models.table import TableStatus,Table
from app.database.database_manager import DatabaseManager

class TableManager():
    '''
    Docstring for TableManager
    '''
    def __init__(self, database_manager:DatabaseManager):
        self.db = database_manager

    def existence_table(self, table_number:int) -> tuple[bool, Table | None]:
        query = """
                SELECT id, table_number, status FROM tables
                WHERE table_number = %s
                """
        res, table = self.db.query_tool(query, params=(table_number,), fetch_one=True)
        if res and table:
            return True, Table(table[0], table[1], table[2])
        return False, None
    
    def add_table(self, table_number:int) -> tuple[bool, str]:
        res, obj = self.existence_table(table_number)
        if not res:
            query = """
                    INSERT INTO tables (table_number, status)
                    VALUES
                    (%s, 'available')
                    RETURNING id
                    """
            result, data = self.db.query_tool(query, params=(table_number,), fetch_one=True)
            if result and data:
                id_table = data[0]
                return True, f"Table added to number {table_number} and ID {id_table}"
            return False, "Database error during insertion"
        return False, f"Table {obj.table_number} has already been added"
    
    def change_status_table(self, table_number:int, new_status: TableStatus) -> tuple[bool, str]:
        res, obj = self.existence_table(table_number)
        if res:
                query = """
                        UPDATE tables
                        SET status = %s
                        WHERE table_number = %s
                        """
                res, data = self.db.query_tool(query, (new_status.value, obj.table_number))
                if res and data:
                    return True, f"Table {obj.table_number} status changed to {new_status.value}."
                return False, "Database error during insertion"
        return False, f"Table number {table_number} does not exist."
    
    def get_all_tables(self) -> tuple[bool, Table | str]:
        query = """
                SELECT id, table_number, status FROM tables
                """
        res, data = self.db.query_tool(query, fetch_all=True)
        if res and data:
            tables = [Table(row[0], row[1], row[2]) for row in data]
            return True, tables
        return False, "Database error during insertion"

    def get_tables_by_status(self, status: TableStatus) -> tuple[bool, list[Table] | str]:
        query = """
                SELECT id, table_number, status FROM tables
                WHERE status = %s
                """
        res, data = self.db.query_tool(query, params=(status.value,), fetch_all=True)
        if res:
            tables = [Table(row[0], row[1], row[2]) for row in data]
            return True, tables
        return False, "Database error during insertion"
    
    def get_table_by_id(self, table_id:int) -> tuple[bool, Table | str]:
        query = """
                SELECT id, table_number, status FROM tables
                WHERE id = %s
                """
        res, data = self.db.query_tool(query, params=(table_id,), fetch_one=True)
        if res and data:
            table_obj = Table(data[0], data[1], data[2])
            return True, table_obj
        return False, "Database error during insertion"
    
    def delete_table(self, table_number:int) -> tuple[bool, str]:
        res_exists, obj = self.existence_table(table_number)
        if not res_exists:
            return False, f"Table {table_number} not found."        
        query = """
                DELETE FROM tables
                WHERE table_number = %s
                """
        res, data = self.db.query_tool(query, params=(table_number,))
        if res:
            return True, f"Table number {table_number} was removed."
        return False, "Database error during insertion"
        