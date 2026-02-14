from app.services import table_logic as tl
from app.services import menu_logic as mu
from app.services import order_logic as ord
from app.utils.validators import get_input

def manage_restaurant():
    while True:
        print("\n--- Restaurant Management ---")
        print("1. Add a new table")
        print("2. Change table status")
        print("3. Remove a table")
        print("4. Add menu item")
        print("5. Change in item prices")
        print("6. Remove item from menu")
        print("7. Back to main menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            t_num = get_input(int, "Enter new table number: ")
            result, text = tl.add_table(t_num)
            print(text)
            input("...")
            
        elif choice == "2":
            t_number = get_input(int, "Enter table number: ")
            new_status = get_input(str, "Enter new table status: ")
            result, text = tl.update_table_status(t_number, new_status)
            print(text)
            input("...")

        elif choice == "3":
            t_num = get_input(int, "Enter table number to remove: ")
            result, text = tl.remove_table(t_num)
            print(text)
            input("...")

        elif choice == "4":
            name = get_input(str, "Please enter the name of the food: ")
            price = get_input(float, "Please enter the price (example: 100.00)")
            result, text = mu.add_menu_item(name, price)
            print(text)
            input("...")

        elif choice == "5":
            name = get_input(str, "Please enter the name of the food: ")
            price = get_input(float, "Please enter the new price (example: 100.00)")
            result, text = mu.edit_menu_item_price(name, price)
            print(text)
            input("...")
        
        elif choice == "6":
            name = get_input(str, "Please enter the name of the food: ")
            result, text = mu.remove_item(name)
            print(text)
            input("...")
        
        elif choice == "7":
            break

        else:
            print("Invalid choice!")

def main_menu():
    while True:
        print("\n=== Restaurant Management System ===")
        print("1. Show Menu")
        print("2. Show Table Status")
        print("3. Add New Order")
        print("4. Update Order Status")
        print("5. View Order Details")
        print("6. Show Daily Sales Report")
        print("7. Manage Restaurant")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            result = mu.show_menu()
            if result:
                for item in result:
                    print(f"ID: {item[0]} | Name: {item[1]} | Price: {item[2]}")
                    input("...")
            elif None in result:
                print("Menu is empty!")
                input("...")

        elif choice == "2":
            result = tl.show_table_status()
            if result:
                for table in result:
                    print(f"ID: {table[0]} | table_number: {table[1]} | status: {table[2]}")
                    input("...")
            elif None in result:
                print("There is no table")
                input("...")

        elif choice == "3":
            t_num = get_input(int,"Enter table number: ")
            result, order_id = ord.add_order(t_num)
            if result:
                print(f"Order created with ID: {order_id}")
                flag = True
                while flag:
                    print("-"*30)
                    mu.show_menu()
                    print("-"*30)
                    print("What item can you add to this order?")
                    item_id = get_input(int, "Please enter the desired item ID: ")
                    quantity = get_input(int, "Please enter the number of items you want: ")
                    result,text = ord.add_item_to_order(order_id, item_id, quantity)
                    print(text)
                    continue_status = get_input(str, "Do you want to add another item?[Y/N]").upper()
                    if continue_status in ["N", "NO", "NA", "NAKHER"]:
                        flag = False
                        input("...")
                    input("...")
            else:
                print(order_id)

        elif choice == "4":
            o_id = get_input(int,"Enter Order ID: ")
            status = get_input(str,"Enter new status (received, preparing, ready, paid): ")
            result, text = ord.update_order_status(o_id, status)
            print(text)
            input("...")

        elif choice == "5":
            o_id = get_input(int, "Enter Order ID to view details: ")
            result_bool, result = ord.show_order_details(o_id)
            if result_bool:
                for name, quantity in result:
                    print(f"{name} --> {quantity}")
            else:
                print(result)

        elif choice == "6":
            result = ord.get_daily_sales_report()
            if result is not None:
                print(f"Get daily sales report -> {result[0]}")
                print("...")

        elif choice == "7":
            manage_restaurant()

        elif choice == "8":
            print("Goodbye!")
            input("...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main_menu()