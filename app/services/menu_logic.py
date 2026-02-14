from utils.db_handler import get_connection,manager_connection

@manager_connection
def add_menu_item(cur, name:str, price:float) -> tuple[bool, str]:
    name = name.capitalize()
    cur.execute(
        "SELECT name FROM menu_items WHERE name = %s ",
        (name,)
    )
    result = cur.fetchone()
    if result is None:
        cur.execute(
            "INSERT INTO menu_items (name, price) VALUES (%s, %s)",
            (name, price)
            )
        return True, "The desired item was successfully added to the menu."
        
    return False, "The desired item is available on the menu."

@manager_connection
def edit_menu_item_price(cur, name:str, price) -> tuple[bool, str]:
    name = name.capitalize()
    cur.execute(
        "SELECT name FROM menu_items WHERE name = %s",
        (name,)
    )
    result = cur.fetchone()
    if result is not None:
        cur.execute(
            "UPDATE menu_items  SET price = %s WHERE name = %s",
            (price, name)
        )
        return True, "The price of the desired item has changed."
    return False, "The desired item was not found."

@manager_connection
def show_menu(cur) -> list:
    cur.execute("SELECT id, name, price FROM menu_items ORDER BY id")
    menu = cur.fetchall()
    if not menu:
        return list()
    else:
        return menu

@manager_connection
def remove_item(cur, name):
    name = name.capitalize()
    cur.execute(
        "SELECT name FROM menu_items WHERE name = %s",
        (name,)
    )
    result = cur.fetchone()
    if result is not None:
        cur.execute(
            "DELETE FROM menu_items WHERE name = %s",
            (name,)
        )
        return True, "The desired item was deleted."
    return False, "The desired item was not found."