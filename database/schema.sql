-- Create users table to restaurant roles.
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    roles VARCHAR(20) NOT NULL CHECK (roles IN ('Admin', 'Waiter'))
);

-- Create tables table to manage restaurant seating status
CREATE TABLE tables (
    id SERIAL PRIMARY KEY,
    table_number INTEGER UNIQUE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'available'
        CHECK (status IN ('available', 'occupied'))
);

-- Create waiter_table to store user_id and table
CREATE TABLE waiter_table(
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    table_id INTEGER REFERENCES tables(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, table_id)
);

-- Create menu_items table to store food names and prices
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    portions_left INTEGER NOT NULL CHECK (portions_left > 0)
);

-- Create orders table to link a table to a specific order session
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    table_id INTEGER REFERENCES tables(id),
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL
        CHECK (status IN ('received','cancelled', 'preparing', 'ready', 'paid'))
);

-- Create order_details to store items and quantities for each order
CREATE TABLE order_details (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES menu_items(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0)
);