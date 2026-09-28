import json

FILE_PATH = "data/inventory.json"

def load_inventory():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def save_inventory(inventory):
    with open(FILE_PATH, "w") as file:
        json.dump(inventory,file,indent=4)

def add_product(inventory,product_id,name,quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    for product in inventory:
        if product["product_id"] == product_id:
            raise ValueError("Product ID already exists")

    product = {
        "product_id": product_id,
        "name": name,
        "quantity": quantity
    }

    inventory.append(product)
    save_inventory(inventory)


def update_stock(inventory,product_id,quantity):
    if quantity < 0:
        raise ValueError("Quantity cannot benegative")

    for product in inventory:
        if product["product_id"] == product_id:
            product["quantity"] = quantity
            save_inventory(inventory)
            return


    raise ValueError("Product not found")


def remove_product(inventory, product_id):
    for product in inventory:
        if product["product_id"] == product_id:
            inventory.remove(product)
            save_inventory(inventory)
            return

    raise ValueError("Product not found")


def search_product(inventory,name):
    results = []
    for product in inventory:
        if name.lower() in product["name"].lower():
            results.append(product)

    return results


def display_inventory(inventory):
    if not inventory:
        print("Inventory is empty")
        return

    print("\n===== INVENTORY =====")

    for product in inventory:
        print(
            f'ID: {product["product_id"]} | '
            f'Name: {product["name"]} | '
            f'Quantity: {product["quantity"]}'
        )