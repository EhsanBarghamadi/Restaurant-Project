class OrderItem:
    def __init__(self, menu_item, quantity: int, id: int = None):
        self.id = id
        self.menu_item = menu_item
        self.quantity = quantity

    def get_total_item_price(self):
        return self.menu_item.price * self.quantity