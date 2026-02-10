-- Create menu_items table to store food names and prices
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);

-- Create tables table to manage restaurant seating status
CREATE TABLE tables (
    id SERIAL PRIMARY KEY,
    table_number INTEGER UNIQUE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'available' -- can be 'available' or 'occupied'
);

-- Create orders table to link a table to a specific order session
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    table_id INTEGER REFERENCES tables(id),
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL -- 'received', 'preparing', 'ready', 'paid' [cite: 419, 420, 421, 422]
);

-- Create order_details to store items and quantities for each order
CREATE TABLE order_details (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    item_id INTEGER REFERENCES menu_items(id),
    quantity INTEGER NOT NULL
);