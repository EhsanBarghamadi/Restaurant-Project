from utils.db_handler import get_connection,manager_connection

@manager_connection
def add_table(cur, table_number:int) -> tuple[bool, str]:
        cur.execute(
          "SELECT table_number FROM tables WHERE table_number = %s",
          (table_number,)
    )
        result = cur.fetchone()
        if result is not None:
             return False, f"The comment table {table_number} is already available."
        cur.execute(
            "INSERT INTO tables (table_number) VALUES (%s)",
            (table_number,)
            )
        return True, f"The table {table_number} was added"
        
@manager_connection
def update_table_status(cur, table_number:int, new_status:str) -> tuple[bool, str]:
    cur.execute(
          "SELECT table_number FROM tables WHERE table_number = %s",
          (table_number,)
    )
    result = cur.fetchone()
    if result is None:
        return False, f"Table #{table_number} does not exist."
    else:
        cur.execute(
            "UPDATE tables SET status = %s WHERE table_number = %s",
            (new_status,table_number)
        )
        return True, f"The status change of table #{table_number} was successful."

@manager_connection
def show_table_status(cur) -> list:
        cur.execute("SELECT * FROM tables")
        tables = cur.fetchall()
        return tables
            

@manager_connection
def remove_table(cur, table_number:int) -> tuple[bool, str]:
    cur.execute(
          "SELECT status FROM tables WHERE table_number = %s",
          (table_number,)
    )
    result = cur.fetchone()
    if result is None:
        return False, f"Table #{table_number} does not exist."
    
    if result[0] == "available":
        cur.execute(
            "DELETE FROM tables WHERE table_number = %s",
            (table_number,)
        )
        return True, "The desired table was deleted."
    else:
         return False,"The requested table is occupied."