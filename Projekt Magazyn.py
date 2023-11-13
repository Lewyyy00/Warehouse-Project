items = [
    {"name": "Laptop", "quantity": 10, "unit": "szt.", "unit_price": 1200.0},
    {"name": "Myszka", "quantity": 50, "unit": "szt.", "unit_price": 30.0},
    {"name": "Monitor", "quantity": 20, "unit": "szt.", "unit_price": 500.0},
        ]

def get_items(items):
    table_format = "{:<8} {:<10} {:<7} {:<8}"
    print(table_format.format('Name', 'Quantity', 'Unit', 'Unit_price (PLN)'))
    print("-" * 40)
    for item in items:
        print(table_format.format(item["name"], item["quantity"], item["unit"], item["unit_price"]))

def add_items(items):
    n = input("Item name:")
    j = input("Item quantity:")
    p = input("Item unit of measure:")
    s = input("Item price in PLN:")
    new_product = {'name':n, "quantity":j, 'unit':p, 'unit_price':s}
    items.append(new_product)
    get_items(items)

def sell_items(items):
    product_name  = input("What would you like to sell? ")
    quantity_to_sell  = int(input("Enter the quantity of the product"))
    for item in items:
        if item["name"] == product_name:
            current_quantity = item["quantity"]
            if quantity_to_sell  <= current_quantity:
                current_quantity -= quantity_to_sell 
                current_unit = item["unit"]
                print(f"You have just sold {quantity_to_sell } {current_unit} and now you got {current_quantity}")
                item['quantity'] = current_quantity
                get_items(items)
            else:
                print("Unfortunately you don't have enough quantity of this product")
            break
        elif item["name"] != product_name:
            print(f"The product:{product_name} doesnt exist")

print("Welcome, you are using warehouse manager")
while True:
    WhatToDo = input("Please choose the number based on your need:\n1.Exit\n2.Show\n3.Add item\n4.Sell item\nI want:")
    if WhatToDo == '1':
        break
    elif WhatToDo == '2':
        get_items(items)
    elif WhatToDo == '3':
        add_items(items)
    elif WhatToDo == '4':
        sell_items(items)
    else:
        print('Sorry, you picked the wrong number. Please choose again 1, 2, 3 or 4')
        continue  









