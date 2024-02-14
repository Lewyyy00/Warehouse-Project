class Product:
    def __init__(self, name, quantity, unit, unit_price):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.unit_price = unit_price

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit} - ${self.unit_price:.2f}"

product_1 = Product("Laptop", 10, "szt.", 1200.0)
product_2 = Product("Myszka", 50, "szt.", 30.0)
product_3 = Product("Monitor", 20, "szt.", 500.0)
product_4 = Product("Lepszy Laptop", 15, "szt.", 2200.0)

products = [product_1, product_2, product_3, product_4]
items = {f'product_{i+1}': product for i, product in enumerate(products)}

