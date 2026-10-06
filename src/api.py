from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from pathlib import Path
import json


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Inventory & Quotation API",
    description="Inventory Management and Quotation API",
    version="1.0.0"
)


# ============================================================
# FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = BASE_DIR / "data" / "inventory.json"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_inventory():
    """
    Load inventory data from JSON file.
    """

    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


def save_inventory(inventory):
    """
    Save inventory data into JSON file.
    """

    with open(FILE_PATH, "w") as file:
        json.dump(
            inventory,
            file,
            indent=4
        )


# ============================================================
# PYDANTIC MODELS
# ============================================================

class Product(BaseModel):
    """
    Complete product model.
    Used for POST and PUT.
    """

    product_id: str = Field(min_length=1)

    name: str = Field(min_length=1)

    quantity: int = Field(
        ge=0
    )

    price: float = Field(
        gt=0
    )


class ProductUpdate(BaseModel):
    """
    Partial product update model.
    Used for PATCH.

    All fields are optional.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=1
    )

    quantity: Optional[int] = Field(
        default=None,
        ge=0
    )

    price: Optional[float] = Field(
        default=None,
        gt=0
    )


# ============================================================
# QUOTATION MODELS
# ============================================================

class QuotationItem(BaseModel):
    """
    One item inside quotation.
    """

    product_id: str = Field(
        min_length=1
    )

    quantity: int = Field(
        gt=0
    )


class QuotationRequest(BaseModel):
    """
    Complete quotation request.
    """

    customer_name: str = Field(
        min_length=1
    )

    items: List[QuotationItem]

    discount_rate: float = Field(
        default=0,
        ge=0,
        le=100
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def home():
    return {"message": "MSME Quotation Engine API chalu chhe"}


# ============================================================
# GET ALL PRODUCTS
# ============================================================

@app.get("/products")
def get_products():

    inventory = load_inventory()

    return {
        "success": True,
        "count": len(inventory),
        "data": inventory
    }


# ============================================================
# GET SINGLE PRODUCT
# ============================================================

@app.get("/products/{product_id}")
def get_product(product_id: str):

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


# ============================================================
# POST - ADD PRODUCT
# ============================================================

@app.post(
    "/products",
    status_code=201
)
def add_product(product: Product):

    inventory = load_inventory()

    # Check duplicate product ID
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


# ============================================================
# PUT - COMPLETE UPDATE
# ============================================================

@app.put("/products/{product_id}")
def update_product(
    product_id: str,
    product: Product
):

    inventory = load_inventory()

    for index, existing_product in enumerate(inventory):

        if existing_product["product_id"] == product_id:

            updated_product = {
                "product_id": product_id,
                "name": product.name,
                "quantity": product.quantity,
                "price": product.price
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


# ============================================================
# PATCH - PARTIAL UPDATE
# ============================================================

@app.patch("/products/{product_id}")
def patch_product(
    product_id: str,
    product: ProductUpdate
):

    inventory = load_inventory()

    for existing_product in inventory:

        if existing_product["product_id"] == product_id:

            # Only take fields actually sent by user
            update_data = product.model_dump(
                exclude_unset=True
            )

            # If body is empty
            if not update_data:

                raise HTTPException(
                    status_code=400,
                    detail="At least one field is required"
                )

            existing_product.update(
                update_data
            )

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


# ============================================================
# DELETE PRODUCT
# ============================================================

@app.delete("/products/{product_id}")
def delete_product(product_id: str):

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


# ============================================================
# POST - CREATE QUOTATION
# ============================================================

@app.post("/quotation")
def create_quotation(
    quotation: QuotationRequest
):

    inventory = load_inventory()

    quotation_items = []

    subtotal = 0

    # --------------------------------------------------------
    # Find products
    # --------------------------------------------------------

    for requested_item in quotation.items:

        product_found = None

        for product in inventory:

            if (
                product["product_id"]
                == requested_item.product_id
            ):

                product_found = product

                break

        # ----------------------------------------------------
        # Product not found
        # ----------------------------------------------------

        if product_found is None:

            raise HTTPException(
                status_code=404,
                detail=(
                    f"Product "
                    f"{requested_item.product_id} "
                    f"not found"
                )
            )

        # ----------------------------------------------------
        # Check stock
        # ----------------------------------------------------

        if (
            requested_item.quantity
            > product_found["quantity"]
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Insufficient stock for "
                    f"{product_found['name']}. "
                    f"Available stock: "
                    f"{product_found['quantity']}"
                )
            )

        # ----------------------------------------------------
        # Calculate item total
        # ----------------------------------------------------

        item_total = (
            product_found["price"]
            * requested_item.quantity
        )

        subtotal += item_total

        quotation_items.append(
            {
                "product_id": product_found["product_id"],
                "name": product_found["name"],
                "quantity": requested_item.quantity,
                "unit_price": product_found["price"],
                "total": item_total
            }
        )

    # --------------------------------------------------------
    # Calculate discount
    # --------------------------------------------------------

    discount_amount = (
        subtotal
        * quotation.discount_rate
        / 100
    )

    # --------------------------------------------------------
    # Final amount
    # --------------------------------------------------------

    final_total = (
        subtotal
        - discount_amount
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "success": True,
        "message": "Quotation created successfully",
        "data": {
            "customer_name": quotation.customer_name,
            "items": quotation_items,
            "subtotal": subtotal,
            "discount_rate": quotation.discount_rate,
            "discount_amount": discount_amount,
            "final_total": final_total
        }
    }