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
        
print("Welcome, you are using warehouse manager")
while True:
    WhatToDo = input("Please choose the number based on your need:\n1.exit \n2.show\nI want:")
    if WhatToDo in ('1','2'):
        break
    print('Sorry, you picked the wrong number please choose again 1 or 2' )
if WhatToDo == '2':
    print(get_items(items))



