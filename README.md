Markdown
# 🍔Restaurant Management System (CLI)

A robust, command-line interface (CLI) application for managing restaurant operations, built with **Python** and **PostgreSQL**.

This project demonstrates core programming concepts including database connectivity (CRUD operations), input validation, decorators, and modular function design.

## 🚀 Features

* **Database Integration:** Uses `psycopg2` to communicate with a PostgreSQL database.
* **Robust Input Validation:** Prevents crashes by validating user inputs (integers, floats, strings) and handling exceptions.
* **Menu Management:** Add new items, update prices, and view the full menu.
* **Table Management:** Add/remove tables and update their status (e.g., available, occupied).
* **Order System:** * Create new orders for specific tables.
    * Add multiple items to an active order.
    * Update order status (received -> preparing -> paid).
* **Reporting:** Generate daily sales reports based on paid orders.

## 🛠️ Technologies Used

* Python 3.x
* PostgreSQL
* Psycopg2 (Database Adapter)

## 📋 Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.x**
2.  **PostgreSQL Database**
3.  **Psycopg2 library:**
    ```bash
    pip install psycopg2
    ```

## ⚙️ Database Setup

1.  Create a PostgreSQL database named `restaurant_db`.
2.  Create the required tables (`menu_items`, `tables`, `orders`, `order_details`) in your database.
3.  Update the `get_connection()` function in `app.py` with your database credentials (user, password, host).

## ▶️ How to Run

Run the script directly from your terminal:

```bash
python main.py
```
<b>😎 New features and improvements are on the way! 
  😅😄😘</b>
</p>


Developed by [Ehsan Barghamadi](https://github.com/EhsanBarghamadi)
