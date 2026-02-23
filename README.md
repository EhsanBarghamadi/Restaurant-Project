# Restaurant Management System 🍽️

A powerful yet simple command-line restaurant management system built with **Python** and **PostgreSQL**. 🚀  
Manage tables, menus, orders, and sales like a pro—perfect for small cafes, diners, or as a starter backend project.

No more spreadsheets. Let the database handle the heavy lifting!

---

## ✨ Why This Project?

- **Efficient & Scalable** – Handles real-time updates for tables and orders with solid validation.
- **User-Friendly CLI** – Interactive menus with pretty-printed tables using `tabulate`.
- **Database-Driven** – PostgreSQL ensures data integrity with constraints and relationships.
- **Extendable Architecture** – Designed for future upgrades like authentication and web interfaces.

---

## 🔥 Features

### 🪑 Table Management
- Add / remove tables
- Update table status (available / occupied)
- View all tables in a clean formatted view

### 📋 Menu Management
- Full CRUD operations for menu items
- Add new dishes 🍕
- Edit prices
- Remove outdated items

### 🛒 Order Handling
- Create new orders
- Add items with quantities
- Update order status (received → paid)
- View detailed order breakdown

### 📊 Reporting
- Daily sales summary
- Subtotals and total revenue
- List of unpaid orders

### ✅ Input Validation
- Prevents invalid data (e.g., negative prices, empty inputs)

### 📝 Logging
- Errors stored in `app.log` for debugging

---

## 🛠️ Prerequisites

- Python 3.8+
- PostgreSQL (local or cloud)
- Required libraries:
  - psycopg2
  - tabulate
  - python-dotenv

---

## 🚀 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/restaurant-management-system.git
cd restaurant-management-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Linux / macOS:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install psycopg2 tabulate python-dotenv
```

### 4️⃣ Configure Environment Variables

Create a `.env` file based on `.env.example`:

```env
DB_NAME=restaurant_db
DB_USERNAME=youruser
DB_PASSWORD=yourpass
DB_HOST=localhost
DB_PORT=5432
```

### 5️⃣ Initialize Database

Create the database manually, then run:

```bash
psql -U youruser -d restaurant_db -f database/schema.sql
```

---

## 📖 Usage

Run the application:

```bash
python main.py
```

### 🧭 Main Menu Highlights

- Show Menu – Browse menu items 🍔
- Add Order – Select table, add items, place order 📝
- Daily Sales – View today's revenue 💰
- Manage Restaurant – Admin mode for managing tables & menu 🔧

Tip: Press Enter to navigate back in most menus.

---

## 🗂️ Project Structure

```
restaurant-management-system/
├── database/
│   └── schema.sql
├── app/
│   ├── services/
│   │   ├── menu_logic.py
│   │   ├── table_logic.py
│   │   └── order_logic.py
│   └── utils/
│       ├── db_handler.py
│       ├── show.py
│       └── validators.py
├── main.py
├── .env.example
├── app.log
└── README.md
```

---

## 🌟 Future Roadmap

### 🔄 Database Triggers
Automate status updates and financial calculations directly inside PostgreSQL.

### 👥 User & Waiter Roles
Authentication system for:
- Managers
- Waiters (each assigned specific tables)

### 🌐 Web Interface
Build a Flask or Django frontend dashboard with sample data to visualize restaurant activity.

---

## 👏 Contributing

1. Fork the repository  
2. Create a new branch  
3. Commit your changes  
4. Open a Pull Request  

Follow PEP8 and add tests when possible.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Acknowledgments

- Inspired by real-world restaurant workflows
- Powered by Python & PostgreSQL
- Built with ❤️ and open-source tools

---

  <br>
  <img src="https://img.shields.io/badge/Status-Work%20in%20Progress-orange?style=for-the-badge&logo=github" alt="Status">
  <br>
  <b>😎 New features and improvements are on the way! 
  😅😄😘</b>
</p>


Developed by [Ehsan Barghamadi](https://github.com/EhsanBarghamadi)