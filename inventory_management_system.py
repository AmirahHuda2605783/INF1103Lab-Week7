
import json
import os
from abc import ABC, abstractmethod


class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class Product(ABC):

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        self.__stock = quantity


    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")


    @abstractmethod
    def get_fulfilment_info(self):
        pass


    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }



class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight


    def get_weight(self):
        return self.__weight


    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")


    def get_fulfilment_info(self):
        return "This product requires physical shipping."


    def calculate_shipping_cost(self):
        return self.__weight * 2.50


    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size


    def get_download_size(self):
        return self.__download_size


    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")


    def get_fulfilment_info(self):
        return "This product is delivered digitally."


    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data



class Inventory:

    def __init__(self):
        self.__products = []


    def add_product(self, product):
        self.__products.append(product)


    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        print("Current Inventory")
        print("------------------------------------------------")

        if len(self.__products) == 0:
            print("Inventory is empty.")

        for product in self.__products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")

            if isinstance(product, CanBeShipped):
                print(
                    f"Shipping Cost: "
                    f"${product.calculate_shipping_cost():.2f}"
                )

            print("------------------------------------------------")

    # Get all products as dictionaries for JSON
    def get_all_products(self):
        return [product.to_dict() for product in self.__products]



def load_inventory():
    inventory = Inventory()

    if os.path.exists("inventory.json"):
        print("inventory.json found.")

        with open("inventory.json", "r") as file:
            data = json.load(file)

        for item in data:

            if item["type"] == "physical":
                product = PhysicalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["weight"]
                )

            elif item["type"] == "digital":
                product = DigitalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["download_size"]
                )

            else:
                print(f"Unknown product type for {item['id']}. Skipping.")
                continue

            inventory.add_product(product)

        print("Inventory loaded successfully.")

    else:
        print("inventory.json not found.")
        print("Starting with an empty inventory.")

    return inventory


def save_inventory(inventory):
    print("Saving inventory...")

    with open("inventory.json", "w") as file:
        json.dump(inventory.get_all_products(), file, indent=4)

    print("Inventory saved successfully to inventory.json.")



print("========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("========================================")

inventory = load_inventory()

while True:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

    option = input("Enter option: ")


    if option == "1":
        inventory.display_all()


    elif option == "2":
        print("Add New Product")

        product_id = input("Product ID: ")


        if inventory.search_product(product_id) is not None:
            print("Product ID already exists.")
            continue

        product_name = input("Product Name: ")
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        print("Select Product Type:")
        print("1. Physical Product")
        print("2. Digital Product")

        product_type = input("Enter option: ")

        if product_type == "1":
            weight = float(input("Weight (kg): "))

            product = PhysicalProduct(
                product_id,
                product_name,
                price,
                stock,
                weight
            )

            print("Physical product created successfully!")

        elif product_type == "2":
            download_size = float(input("Download Size (MB): "))

            product = DigitalProduct(
                product_id,
                product_name,
                price,
                stock,
                download_size
            )

            print("Digital product created successfully!")

        else:
            print("Invalid product type.")
            continue

        inventory.add_product(product)
        print("Product added successfully!")

    elif option == "3":
        print("Update Stock")

        product_id = input("Enter Product ID: ")
        product = inventory.search_product(product_id)

        if product is not None:
            print("Product Found:")
            print(f"Name: {product.get_name()}")
            print(f"Current Stock: {product.get_stock()}")

            new_stock = int(input("New Stock Quantity: "))
            product.update_stock(new_stock)

            print("Stock updated successfully!")

        else:
            print("Product not found.")


    elif option == "4":
        print("Search Product")

        product_id = input("Enter Product ID: ")
        product = inventory.search_product(product_id)

        if product is not None:
            print("Product Found")
            print("------------------------------------------------")

            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")

            if isinstance(product, CanBeShipped):
                print(
                    f"Shipping Cost: "
                    f"${product.calculate_shipping_cost():.2f}"
                )

            print("------------------------------------------------")

        else:
            print("Product not found.")


    elif option == "5":
        save_inventory(inventory)


    elif option == "6":
        print("Saving inventory before exit...")
        save_inventory(inventory)

        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break

    else:
        print("Invalid option. Please try again.")
