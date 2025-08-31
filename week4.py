import os
import random
from datetime import datetime
from abc import ABC, abstractmethod

def get_now(): # used for consistent timestamps
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Archivable(ABC): # abstract base class, responsible for logging
    def __init__(self, obj, name):
        obj_name = obj.__class__.__name__ # saves the name of the object
        self.__log_file_name = f"{obj_name}_{name}.txt"
        log_exists = os.path.exists(self.__log_file_name)
        self.__log_file = open(self.__log_file_name, "w") # creates a log file
        if not log_exists:
            self.__log_file.write(f"{get_now()} - {obj_name} {name} created\n") # initialises the log file
        self._log_init()

    def __del__(self): # upon deletion, closes the log file
        self.__log_file.close()

    def _delete_log_file(self): # deletes the log file
        os.remove(self.__log_file_name)

    @abstractmethod
    def _log_init(self): # abstract method for adding class-specific information to the log file
        pass

    def update_archive(self, log_entry): # creates a timestamped entry in the log file
        self.__log_file.write(f"{get_now()} - {log_entry}\n")


class Product(Archivable): # responsible for storing product information
    def __init__(self, name, price):
        self.name = name
        self._price = price
        super().__init__(self, name) # initialises the log file

    def _log_init(self): # adds class-specific information in the log file
        self.update_archive(f"Initial price: {self.price} $")

    @property
    def price(self): # getter decorator for price
        return self._price

    @price.setter
    def price(self, new_price): # setter decorator for price
        self._price = new_price # updates the price
        self.update_archive(f"Price has been updated to: {new_price} $") # updates the log file

class Customer(Archivable): # responsible for storing customer information and placing orders
    def __init__(self, name, address):
        self.name = name
        self._address = address
        self.orders = []
        super().__init__(self, name) # initialises the log file

    def __del__(self):
        self._delete_log_file() # delete sensitive log information upon deletion

    def _log_init(self): # adds class-specific information in the log file
        self.update_archive(f"Initial address: {self.address}")

    def _create_order(self, positions): # protected method for creating an order object from a list of Products
        order = Order(self, positions)
        self.orders.append(order) # adds the order to the customer's order list
        self.update_archive(f"Order #{order.order_nr} placed") # updates the customer's log file
        return order

    @property
    def address(self): # getter decorator for address
        return self._address

    @address.setter
    def address(self, new_address): # setter decorator for address
        self._address = new_address # updates the address
        self.update_archive(f"Address has been updated to: {new_address}") # updates the log file

    def place_order(self, positions): # responsible for placing an order
        shipping_fee = Product("Shipping", 2)
        positions.append(shipping_fee) # adds the standard shipping fee to the positions
        return self._create_order(positions) # creates the order object


class PremiumCustomer(Customer): # responsible for storing premium customer information
    def __init__(self, name, address):
        super().__init__(name, address) # initialises the log file

    def _log_init(self): # adds class-specific information in the log file
        self.update_archive("Customer is a Premium Customer!")
        super()._log_init() # adds class-specific information of the parent class in the log file

    def place_order(self, positions): # responsible for placing an order without shipping fee (premium feature)
        return self._create_order(positions)

class Address: # responsible for storing address information
    def __init__(self, street, house_nr, city):
        self.street = street
        self.house_nr = house_nr
        self.city = city

    def __str__(self): # overwrites the string representation of the address object
        return f"{self.street} {self.house_nr}, {self.city}"


class Order(Archivable): # responsible for storing order information and calculating total price
    def __init__(self, owner, positions):
        self.order_nr = random.randint(100, 999) # simplified logic for generating order numbers
        self.owner = owner
        self.positions = positions
        self._status = "Created"
        super().__init__(self, f"#{self.order_nr}") # initialises the log file

    def _log_init(self): # adds class-specific information in the log file
        for position in self.positions: # adds each position to the log file
            self.update_archive(f"{position.name} added to Order")
        self.calculate_total_price() # adds total price to the log file

    def add_item(self, position): # adds a single position to the order
        self.positions.append(position)
        self.update_archive(f"{position.name} added to order") # updates the log file
        self.calculate_total_price() # adds the new total price to the log file

    def calculate_total_price(self): # calculates the total price of the order
        total_price = 0
        for position in self.positions:
            total_price += position.price
        self.update_archive(f"ORDER TOTAL: {total_price} $") # updates the log file with the total price

    @property
    def status(self): # getter decorator for status
        return self._status

    @status.setter
    def status(self, new_status): # setter decorator for status
        self._status = new_status # updates the status
        self.update_archive(f"Status has been updated to: {new_status}") # updates the log file
        self.owner.update_archive(f"Order #{self.order_nr} has been updated to: {new_status}") # updates owner's log file


bread = Product("Bread", 2.5)
salami = Product("Salami", 3)
salami.price = 2

kate = Customer("Kate", Address("Tropicana St", 9, "Miami"))
kate.address = Address("Yale Ave", 2, "Denver")
kate_order = kate.place_order([bread, salami])
kate_order.add_item(bread)
kate_order.status = "SHIPPED"
kate_order.status = "COMPLETED"

john = PremiumCustomer("John", Address("Jackson Blvd", 15, "Chicago"))
john_order = john.place_order([salami])
john_order.status = "SHIPPED"
john_order.status = "COMPLETED"