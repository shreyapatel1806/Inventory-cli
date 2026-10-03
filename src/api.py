from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
import json


app = FastAPI(
    title="Inventory Management API",
    description="API for Inventory CLI",
    version="1.0.0"
)


# ==========================================
# JSON FILE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "inventory.json"


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def load_inventory():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def save_inventory(inventory):
    with open(FILE_PATH, "w") as file:
        json.dump(inventory, file, indent=4)


# ==========================================
# PYDANTIC MODELS
# ==========================================

class Product(BaseModel):
    product_id: int
    name: str = Field(min_length=1)
    quantity: int = Field(ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    quantity: Optional[int] = Field(default=None, ge=0)


# ==========================================
# GET - ALL PRODUCTS
# ==========================================

@app.get("/products")
def get_products():

    inventory = load_inventory()

    return {
        "success": True,
        "count": len(inventory),
        "data": inventory
    }


# ==========================================
# GET - SINGLE PRODUCT
# ==========================================

@app.get("/products/{product_id}")
def get_product(product_id: int):

    inventory = load_inventory()

    for product in inventory:

        if product["product_id"] == product_id:

            return {
                "success": True,
                "data": product
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# ==========================================
# POST - ADD PRODUCT
# ==========================================

@app.post("/products", status_code=201)
def add_product(product: Product):

    inventory = load_inventory()

    # Check duplicate ID
    for existing_product in inventory:

        if existing_product["product_id"] == product.product_id:

            raise HTTPException(
                status_code=400,
                detail="Product ID already exists"
            )

    new_product = product.model_dump()

    inventory.append(new_product)

    save_inventory(inventory)

    return {
        "success": True,
        "message": "Product added successfully",
        "data": new_product
    }


# ==========================================
# PUT - COMPLETE UPDATE
# ==========================================

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):

    inventory = load_inventory()

    for index, existing_product in enumerate(inventory):

        if existing_product["product_id"] == product_id:

            updated_product = {
                "product_id": product_id,
                "name": product.name,
                "quantity": product.quantity
            }

            inventory[index] = updated_product

            save_inventory(inventory)

            return {
                "success": True,
                "message": "Product completely updated",
                "data": updated_product
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# ==========================================
# PATCH - PARTIAL UPDATE
# ==========================================

@app.patch("/products/{product_id}")
def patch_product(
    product_id: int,
    product: ProductUpdate
):

    inventory = load_inventory()

    for existing_product in inventory:

        if existing_product["product_id"] == product_id:

            update_data = product.model_dump(
                exclude_unset=True
            )

            existing_product.update(update_data)

            save_inventory(inventory)

            return {
                "success": True,
                "message": "Product partially updated",
                "data": existing_product
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# ==========================================
# DELETE - DELETE PRODUCT
# ==========================================

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    inventory = load_inventory()

    for index, product in enumerate(inventory):

        if product["product_id"] == product_id:

            deleted_product = inventory.pop(index)

            save_inventory(inventory)

            return {
                "success": True,
                "message": "Product deleted successfully",
                "data": deleted_product
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Inventory API is running"
    }