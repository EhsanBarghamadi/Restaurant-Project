from app.models.user import Users, UserRoles
from app.models.table import Table
from app.database.database_manager import DatabaseManager

class UserManager:
    """
    Manager for handling users: registration, login, deletion, password change, and table assignments.
    """
    def __init__(self, database_manager:DatabaseManager):
        self.db = database_manager

    def existence_user(self, username: str) -> tuple[bool, Users | None]:
        username = username.lower()
        query = """
                SELECT id, username, password, roles FROM users
                WHERE username = %s
                """
        res, data = self.db.query_tool(query, params=(username,), fetch_one=True)
        if res and data:
                if data[3] == "waiter":
                    query ="""
                            SELECT tables.id, tables.table_number, status 
                            FROM users
                            INNER JOIN waiter_table
                            ON users.id = waiter_table.user_id
                            INNER JOIN tables
                            ON waiter_table.table_id = tables.id
                            WHERE users.id = %s
                            """
                    result, info = self.db.query_tool(query, params=(data[0],), fetch_all=True)
                    if result and not any(None in item for item in info):
                        assigned_tables = []
                        for item in info:
                            assigned_tables.append(Table(item[0], item[1], item[2]))
                        user_obj = Users(data[0], data[1], data[2], data[3],assigned_tables)
                        return True, user_obj
                user_obj = Users(data[0], data[1], data[2], data[3])
                return True, user_obj
        return False, None
    
    def register(self, username: str, password: str, role: UserRoles) -> tuple[bool, object | str]:
        username = username.lower()
        res, data = self.existence_user(username)
        if res:
            return False, f"Username {data.username} exists."
        query = """
                INSERT INTO users (username, password, roles)
                VALUES
                (%s, %s, %s)
                RETURNING id
                """
        result, info = self.db.query_tool(query, params=(username, password, role.value), fetch_one=True, end=True)
        if result and info:
             new_user = Users(info[0], username, password, role)
             return True, new_user
        return False, "Database error during insertion"
    
    def delete_user(self, username: str) -> tuple[bool, str]:
        username = username.lower()
        res, data = self.existence_user(username)
        if not res:
            return False, f"Username {username} not exists."
        query = """
                DELETE FROM users
                WHERE id = %s
                """
        result, info = self.db.query_tool(query, params=(data.id,))
        if result:
            return True, f"Username {username} was deleted."
        return False, "Database error during insertion"
    
    def change_password(self, username: str, old_password: str, new_password: str) -> tuple[bool, str]:
        username = username.lower()
        res, data = self.existence_user(username)
        if not data:
            return False, f"Username {username} not exists."
        if res:
                if old_password == data.password:
                    query = """
                            UPDATE users
                            SET password = %s
                            WHERE username = %s
                            """
                    output, finding = self.db.query_tool(query, params=(new_password, data.username))
                    if output:
                        return True, f"Username {username}'s password has been changed successfully."
                    return False, "Database error during update"              
                return False, f"Old password does not match."                
        return False, "Database error during insertion"
    
    def login(self, username:str, password:str) -> tuple[bool, Users | None, str]:
        username = username.lower()
        res, data = self.existence_user(username)
        if  not res or data is None:
            return False, None, f"Username {username} not exists."
        if data.password == password:
             return True, data, "Login was successful."
        return False, None, "Incorrect password entered."
    
    def get_assign_tables_all_waiter(self) -> tuple[bool, list[Users] | str]:
            query = """
                    SELECT username FROM users
                    WHERE roles = 'waiter'
                    """
            result, username_waiter = self.db.query_tool(query,fetch_all=True)
            if result:
                info_waiter = []
                for (username,) in username_waiter:
                    resu, user_obj = self.existence_user(username)
                    info_waiter.append(user_obj)
                return True, info_waiter
            return False, "Database error during insertion"

    def assign_table_to_waiter(self, waiter_username: str, table_id) -> tuple[bool, str]:
        res, obj_waiter = self.existence_user(waiter_username)
        if not res or obj_waiter is None:
            return False, f"Username {waiter_username} not exists."
        if obj_waiter.roles.value == "admin":
            return False, "Cannot assign a table to the admin."
        query = """
                DELETE FROM waiter_table
                WHERE table_id = %s
                """ 
        resu, info = self.db.query_tool(query, params=(table_id,))
        if resu:
            query = """
                    INSERT INTO  waiter_table (user_id, table_id)
                    VALUES
                    (%s, %s)
                    """ 
            result, info = self.db.query_tool(query, params=(obj_waiter.id, table_id))
            if result:
                return True, f"Table ID {table_id} was assigned to {obj_waiter.username}."
        return False, info

    def remove_table_from_waiter(self, waiter_username: str, table_id) -> tuple[bool, str]:
        res, obj_waiter = self.existence_user(waiter_username)
        if not res or obj_waiter is None:
            return False, f"Username {waiter_username} not exists."
        if obj_waiter.roles.value == "admin":
            return False, "The logged in user is admin."
        query = """
                DELETE FROM waiter_table
                WHERE user_id = %s
                AND table_id = %s
                """ 
        resu, info = self.db.query_tool(query, params=(obj_waiter.id, table_id))
        if resu:
                return True, f"The allocated table {table_id} was successfully deleted."
        return False, info