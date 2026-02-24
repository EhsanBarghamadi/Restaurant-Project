from enum import Enum

class TableStatus(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"

class Table:
    def __init__(self, id: int, table_number: int, status: str):
        self.id = id
        self.table_number = table_number
        self.status = TableStatus(status)