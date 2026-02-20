from app.database.database_manager import DatabaseManager
from enum import Enum

db = DatabaseManager()

class UserRoles(Enum):
    ADMIN = 'admin'
    WAITER = 'waiter'

class Users():
    """
    Docstring for Users
    """
    def __init__(self, id, username, password, roles: object):
        self.id = id
        self.username = username
        self.password = password
        self.roles = UserRoles(roles)
    