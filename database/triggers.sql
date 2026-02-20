CREATE OR REPLACE FUNCTION available_table_after_paid()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'paid' AND OLD.status != 'paid'
    THEN NEW.order_time := NOW();
    UPDATE tables
    SET status = 'available'
    WHERE id = NEW.table_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER available_table
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION available_table_after_paid();

COMMENT ON TRIGGER available_table ON orders IS 'Availbling up the table after paying for the order';


CREATE OR REPLACE FUNCTION decrease_portions_left()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE menu_items
    SET portions_left = portions_left - NEW.quantity
    WHERE id = NEW.menu_item_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER portions_left_decrease
AFTER INSERT ON order_details
FOR EACH ROW
EXECUTE FUNCTION decrease_portions_left();

COMMENT ON TRIGGER portions_left_decrease ON order_details IS 'Reducing inventory after placing an order';


CREATE OR REPLACE FUNCTION return_stock_on_cancel()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'cancelled' AND OLD.status != 'cancelled' THEN
        UPDATE menu_items
        SET portions_left = portions_left + od.quantity
        FROM order_details od
        WHERE menu_items.id = od.item_id 
        AND od.order_id = NEW.id;
        UPDATE tables
        SET status = 'available'
        WHERE id = NEW.table_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_cancel_order
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION return_stock_on_cancel();

COMMENT ON TRIGGER trg_cancel_order ON orders IS 'Reverting the table and inventory to their original state after canceling an order';


CREATE OR REPLACE FUNCTION check_portions_left()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantity > OLD.quantity
    THEN UPDATE menu_items
    SET portions_left = portions_left - (NEW.quantity - OLD.quantity)
    WHERE menu_items.id = NEW.menu_item_id;
    ELSIF NEW.quantity < OLD.quantity
    THEN UPDATE menu_items
    SET portions_left = portions_left + (OLD.quantity - NEW.quantity)
    WHERE menu_items.id = NEW.menu_item_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER portions_left_check
AFTER UPDATE ON order_details
FOR EACH ROW
EXECUTE FUNCTION check_portions_left();

COMMENT ON TRIGGER portions_left_check ON order_details IS 'Fixing inventory after changing an order';

CREATE OR REPLACE FUNCTION return_stock_on_delete()
RETURNS TRIGGER AS $$
BEGIN 
    UPDATE menu_items
    SET portions_left = portions_left + OLD.quantity
    WHERE id = OLD.menu_item_id;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_return_stock_on_delete
AFTER DELETE ON order_details
FOR EACH ROW
EXECUTE FUNCTION return_stock_on_delete();

COMMENT ON TRIGGER trg_return_stock_on_delete ON order_details IS 'Return inventory to warehouse if an item is physically removed from an order';