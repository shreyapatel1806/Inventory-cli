from inventory import (
    load_inventory,
    add_product,
    update_stock,
    remove_product,
    search_product,
    display_inventory
)


def main():

    inventory = load_inventory()

    while True:

        print(
            "\n================ Inventory Management ================"
        )

        print("1. Add Product")
        print("2. Update Stock")
        print("3. Remove Product")
        print("4. View Inventory")
        print("5. Search Inventory")
        print("6. Exit")

        choice = input(
            "Enter your choice: "
        )

        try:

            # ==================================================
            # ADD PRODUCT
            # ==================================================

            if choice == "1":

                product_id = input(
                    "Product ID: "
                ).strip()

                name = input(
                    "Product Name: "
                ).strip()

                quantity = int(
                    input(
                        "Quantity: "
                    )
                )

                price = float(
                    input(
                        "Price: "
                    )
                )

                add_product(
                    inventory,
                    product_id,
                    name,
                    quantity,
                    price
                )

                print(
                    "Product added successfully."
                )

            # ==================================================
            # UPDATE STOCK
            # ==================================================

            elif choice == "2":

                product_id = input(
                    "Product ID: "
                ).strip()

                quantity = int(
                    input(
                        "New Quantity: "
                    )
                )

                update_stock(
                    inventory,
                    product_id,
                    quantity
                )

                print(
                    "Stock updated successfully."
                )

            # ==================================================
            # REMOVE PRODUCT
            # ==================================================

            elif choice == "3":

                product_id = input(
                    "Product ID: "
                ).strip()

                remove_product(
                    inventory,
                    product_id
                )

                print(
                    "Product removed successfully."
                )

            # ==================================================
            # VIEW INVENTORY
            # ==================================================

            elif choice == "4":

                display_inventory(
                    inventory
                )

            # ==================================================
            # SEARCH
            # ==================================================

            elif choice == "5":

                name = input(
                    "Enter Product name: "
                ).strip()

                results = search_product(
                    inventory,
                    name
                )

                if results:

                    display_inventory(
                        results
                    )

                else:

                    print(
                        "Product not found."
                    )

            # ==================================================
            # EXIT
            # ==================================================

            elif choice == "6":

                print(
                    "Application closed."
                )

                break

            # ==================================================
            # INVALID OPTION
            # ==================================================

            else:

                print(
                    "Invalid choice."
                )

        except ValueError as error:

            print(
                "Error:",
                error
            )


if __name__ == "__main__":

    main()