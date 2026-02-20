from app.models.user import Users, UserRoles
from app.models.waiter import Waiter
from app.models.table import Table
from app.database.database_manager import DatabaseManager

db = DatabaseManager()

class UserManager:
    """
    Manager for handling users: registration, login, deletion, password change, and table assignments.
    """
    def __init__(self):
        self.all_user = []
        self.load_all()

    def load_all(self):
        query = """
                SELECT id, username, password, roles FROM users
                """
        result, fetch = db.query_tool(query, fetch=True)
        if result:
            for item in fetch:
                if item[3] == UserRoles.WAITER:
                    waiter = Waiter(item[0], item[1], item[2], UserRoles(item[3]))
                    self.all_user.append(waiter)
                else:
                    user = Users(item[0], item[1], item[2], UserRoles(item[3]))
                    self.all_user.append(user)
            return self.all_user
    
    def existence_user(self, username: str) -> tuple[bool, Users | None]:
        username = username.lower()
        find_user = [user for user in self.all_user if user.username.lower() == username]
        if find_user:
            return True, find_user[0]
        return False, None

    def register(self, username: str, password: str, role: UserRoles) -> tuple[bool, object | None]:
        query = """
                INSERT INTO users(username, password, roles)
                VALUES
                (%s, %s, %s)
                RETURNING id
                """
        result, fetch = db.query_tool(query, params=(username, password, role.value), fetch=True)
        if result:
            if role == UserRoles.WAITER:
                new_user = Waiter(fetch[0][0], username, password, UserRoles(role))
                self.all_user.append(new_user)
                return True, new_user
            else:
                new_user = Users(fetch[0], username, password, UserRoles(role))
                self.all_user.append(new_user)
                return True, new_user
        return False, None

    def login(self, username: str, password: str) -> tuple[bool, Users | str]:
        username = username.lower()
        find_username = [user for user in self.all_user if user.username.lower() == username]
        if find_username:
            if find_username[0].password == password:
                return True, find_username[0]
            return False, "Incorrect password."
        return False, "User does not exist."

    def delete_user(self, username: str) -> tuple[bool, str]:
        username = username.lower()
        find_username = [user for user in self.all_user if user.username.lower() == username]
        if find_username:
            query = """
                    DELETE FROM users 
                    WHERE id = %s
                    """
            result, test = db.query_tool(query,(find_username[0].id,))
            if result:
                self.all_user.remove(find_username[0])
                return True, f"User {username} deleted."
            return False, "Database error."
        return False, "User does not exist."
    

    def change_password(self, username: str, old_password: str, new_password: str) -> tuple[bool, str]:
        username = username.lower()
        find_username = [user for user in self.all_user if user.username.lower() == username]
        if find_username:
            if find_username[0].password == old_password:
                query = """
                        UPDATE users
                        SET password = %s
                        WHERE id = %s
                        """
                result, text = db.query_tool(query, (new_password, find_username[0].id))
                if result:
                    find_username[0].password = new_password
                    return True, "Password changed successfully."
            return False, "Incorrect old password"
        return False, "User does not exist."

    def assign_table_to_waiter(self, waiter_username: str, table: Table) -> tuple[bool, str]:
        username = waiter_username.lower()
        find_username = [user for user in self.all_user if user.username.lower() == username]
        if find_username and find_username[0].roles.value == UserRoles.WAITER:
            query = """
                    INSERT INTO waiter_table(user_id, table_id)
                    VALUES
                    (%s, %s)
                    """
            result, text = db.query_tool(query, (find_username[0].id, table.id))
            if result:
                find_username[0].get_assigned_tables()
                return True, "Table assigned"
            return False, "Database error."
        return False, "Waiter does not exist or not a waiter."

    def remove_table_from_waiter(self, waiter_username: str, table_id: int) -> tuple[bool, str]:
        username = waiter_username.lower()
        find_username = [user for user in self.all_user if user.username.lower() == username]
        if find_username and find_username[0].roles.value == UserRoles.WAITER:
            query = """
                    DELETE FROM waiter_table
                    WHERE table_id = %s AND user_id = %s
                    """
            result, text = db.query_tool(query, (table_id, find_username[0].id))
            if result:
                find_username[0].get_assigned_tables()
                return True, "Table removed"
            return False, "Database error."
        return False, "Waiter does not exist."