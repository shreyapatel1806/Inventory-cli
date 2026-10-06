import json
from pathlib import Path


# ============================================================
# FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = BASE_DIR / "data" / "inventory.json"


# ============================================================
# LOAD INVENTORY
# ============================================================

def load_inventory():

    try:

        with open(FILE_PATH, "r") as file:

            return json.load(file)

    except FileNotFoundError:

        return []


# ============================================================
# SAVE INVENTORY
# ============================================================

def save_inventory(inventory):

    with open(FILE_PATH, "w") as file:

        json.dump(
            inventory,
            file,
            indent=4
        )


# ============================================================
# ADD PRODUCT
# ============================================================

def add_product(
    inventory,
    product_id,
    name,
    quantity,
    price
):

    if not product_id:

        raise ValueError(
            "Product ID is required"
        )

    if not name:

        raise ValueError(
            "Product name is required"
        )

    if quantity <= 0:

        raise ValueError(
            "Quantity must be greater than 0"
        )

    if price <= 0:

        raise ValueError(
            "Price must be greater than 0"
        )

    # Check duplicate ID
    for product in inventory:

        if product["product_id"] == product_id:

            raise ValueError(
                "Product ID already exists"
            )

    product = {
        "product_id": product_id,
        "name": name,
        "quantity": quantity,
        "price": price
    }

    inventory.append(product)

    save_inventory(inventory)


# ============================================================
# UPDATE STOCK
# ============================================================

def update_stock(
    inventory,
    product_id,
    quantity
):

    if quantity < 0:

        raise ValueError(
            "Quantity cannot be negative"
        )

    for product in inventory:

        if product["product_id"] == product_id:

            product["quantity"] = quantity

            save_inventory(inventory)

            return

    raise ValueError(
        "Product not found"
    )


# ============================================================
# REMOVE PRODUCT
# ============================================================

def remove_product(
    inventory,
    product_id
):

    for product in inventory:

        if product["product_id"] == product_id:

            inventory.remove(product)

            save_inventory(inventory)

            return

    raise ValueError(
        "Product not found"
    )


# ============================================================
# SEARCH PRODUCT
# ============================================================

def search_product(
    inventory,
    name
):

    results = []

    for product in inventory:

        if name.lower() in product["name"].lower():

            results.append(product)

    return results


# ============================================================
# DISPLAY INVENTORY
# ============================================================

def display_inventory(inventory):

    if not inventory:

        print("\nInventory is empty.")

        return

    print("\n================ INVENTORY ================")

    for product in inventory:

        print(
            f"ID: {product['product_id']} | "
            f"Name: {product['name']} | "
            f"Quantity: {product['quantity']} | "
            f"Price: ₹{product['price']}"
        )

    print("===========================================")