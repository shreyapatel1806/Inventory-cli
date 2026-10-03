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

        print("\n================ Inventory Management ================")
        print("1. Add Product")
        print("2. Update Stock")
        print("3. Remove Product")
        print("4. View Inventory")
        print("5. Search Inventory")
        print("6. Exit")

        choice = input("Enter your choice: ")

        try:

            if choice == "1":

                product_id = int(
                    input("Product ID: ")
                )

                name = input("Product Name: ")

                quantity = int(
                    input("Quantity: ")
                )

                add_product(
                    inventory,
                    product_id,
                    name,
                    quantity
                )

                print("✅ Product added successfully")


            elif choice == "2":

                product_id = int(
                    input("Product ID: ")
                )

                quantity = int(
                    input("New Quantity: ")
                )

                update_stock(
                    inventory,
                    product_id,
                    quantity
                )

                print("✅ Stock updated successfully")


            elif choice == "3":

                product_id = int(
                    input("Product ID: ")
                )

                remove_product(
                    inventory,
                    product_id
                )

                print("✅ Product removed successfully")


            elif choice == "4":

                display_inventory(inventory)


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


            elif choice == "6":

                print("Application closed.")
                break


            else:

                print("❌ Invalid choice")


        except ValueError as error:

            print("❌ Error:", error)


if __name__ == "__main__":
    main()