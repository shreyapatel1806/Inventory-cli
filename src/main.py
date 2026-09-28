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
        print("\n===========================================")
        print("1. Add Product")
        print("2. Update Stock")
        print("3. Remove Product")
        print("4. View Inventory")
        print("5. Search Inventory")
        print("6. Exit")

        choice = input("Enter your choice: ")

        try:

            # add 
            if choice == "1":
                product_id = int(
                    input("Product ID: ")
                )

                name = input("Product Name: ")

                quantity = int(input("Quantity: "))

                add_product(
                    inventory,
                    product_id,
                    name,
                    quantity
                )

                print("✅ product added successfully")


            # Update Stock
            elif choice == "2":

                product_id = int(input("Product ID: "))

                quantity = int(input("New Quantity: "))

                update_stock(
                    inventory,
                    product_id,
                    quantity
                )

                print("✅ Stock updated successfully")


            # Remove Product
            elif choice == "3":
                product_id = int(input("Product ID: "))

                remove_product(
                    inventory,
                    product_id
                ) 

                print("✅ Product removed successfully")


            # View Inventory
            elif choice == "4":

                display_inventory(inventory)


            # Search Product
            elif choice == "5":
                name = input("Enter Product name: ")

                results = search_product(
                    inventory,
                    name
                )
                if results:
                    display_inventory(results)
                else:
                    print("❌ Product not found")


            # Exit
            elif choice == "6":
                print("Application closed.")
                break

            else:
                print("❌ Invalid choice")

        except ValueError as error:
            print("❌ Error:",error)


# if __name__ == "__main__":
#     main()

main()