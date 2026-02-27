from enum import Enum

class UserRoles(Enum):
    ADMIN = 'admin'
    WAITER = 'waiter'

class Users():
    """
    Docstring for Users
    """
    def __init__(self, id, username, password, roles: str, assigned_tables: list = None):
        self.id = id
        self.username = username
        self.password = password
        self.roles = UserRoles(roles)
        self.assigned_tables = assigned_tables if assigned_tables else list()