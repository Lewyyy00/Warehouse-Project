items = [
    {"name": "Laptop", "quantity": 10, "unit": "szt.", "unit_price": 1200.0},
    {"name": "Myszka", "quantity": 50, "unit": "szt.", "unit_price": 30.0},
    {"name": "Monitor", "quantity": 20, "unit": "szt.", "unit_price": 500.0},
        ]

def get_items(items):
    table_format = "{:<8} {:<10} {:<7} {:<8}"
    print(table_format.format('Name', 'Quantity', 'Unit', 'Unit_price'))
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
  
print("Welcome, you are using warehouse manager")
while True:
    WhatToDo = input("Please choose the number based on your need:\n1.Exit\n2.Show\n3.Add item\nI want:")
    if WhatToDo == '1':
        break
    elif WhatToDo == '2':
        get_items(items)
    elif WhatToDo == '3':
        add_items(items)
    else:
        print('Sorry, you picked the wrong number. Please choose again 1, 2, or 3')
        continue  









