import os
import random
from datetime import datetime
from abc import ABC, abstractmethod

def get_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Archivable(ABC):
    def __init__(self, obj, name):
        obj_name = obj.__class__.__name__
        self.__log_file_name = f"{obj_name}_{name}.txt"
        log_exists = os.path.exists(self.__log_file_name)
        self.__log_file = open(self.__log_file_name, "w")
        if not log_exists:
            self.__log_file.write(f"{get_now()} - {obj_name} {name} created\n")
        self._log_init()

    def __del__(self):
        self.__log_file.close()

    def _delete_log_file(self):
        os.remove(self.__log_file_name)

    @abstractmethod
    def _log_init(self):
        pass

    def update_archive(self, log_entry):
        self.__log_file.write(f"{get_now()} - {log_entry}\n")


class Product(Archivable):
    def __init__(self, name, price):
        self.name = name
        self._price = price
        super().__init__(self, name)

    def _log_init(self):
        self.update_archive(f"Current price: {self.price} $")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        self._price = new_price
        self.update_archive(f"Price has been updated to: {new_price} $")

class Customer(Archivable):
    def __init__(self, name, address):
        self.name = name
        self._address = address
        self.orders = []
        super().__init__(self, name)

    # def __del__(self):
    #     self._delete_log_file()

    def _log_init(self):
        self.update_archive(f"Current address: {self.address}")

    def _create_order(self, positions):
        order = Order(self, positions)
        self.orders.append(order)
        self.update_archive(f"Order #{order.order_nr} placed")
        return order

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, new_address):
        self._address = new_address
        self.update_archive(f"Address has been updated to: {new_address}")

    def place_order(self, positions):
        shipping_fee = Product("Shipping", 2)
        positions.append(shipping_fee)
        return self._create_order(positions)


class PremiumCustomer(Customer):
    def __init__(self, name, address):
        super().__init__(name, address)

    def _log_init(self):
        self.update_archive("Customer is a Premium Customer!")
        super()._log_init()

    def place_order(self, positions):
        return self._create_order(positions)

class Address:
    def __init__(self, street, house_nr, city):
        self.street = street
        self.house_nr = house_nr
        self.city = city

    def __str__(self):
        return f"{self.street} {self.house_nr}, {self.city}"


class Order(Archivable):
    def __init__(self, owner, positions):
        self.order_nr = random.randint(100, 999)
        self.owner = owner
        self.positions = positions
        self._status = "Created"
        super().__init__(self, f"#{self.order_nr}")

    def _log_init(self):
        for position in self.positions:
            self.update_archive(f"{position.name} added to Order")
        self.calculate_total_price()

    def add_item(self, position):
        self.positions.append(position)
        self.update_archive(f"{position.name} added to order")
        self.calculate_total_price()

    def calculate_total_price(self):
        total_price = 0
        for position in self.positions:
            total_price += position.price
        self.update_archive(f"ORDER TOTAL: {total_price} $")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status
        self.update_archive(f"Status has been updated to: {new_status}")
        self.owner.update_archive(f"Order #{self.order_nr} has been updated to: {new_status}")


bread = Product("Bread", 2.5)
salami = Product("Salami", 3)
salami.price = 2

# kate = Customer("Kate", Address("Tropicana St", 9, "Miami"))
# kate.address = Address("Yale Ave", 2, "Denver")
# kate_order = kate.place_order([bread, salami])
# kate_order.add_item(bread)
# kate_order.status = "SHIPPED"
# kate_order.status = "COMPLETED"

john = PremiumCustomer("John", Address("Jackson Blvd", 15, "Chicago"))
john_order = john.place_order([salami])
john_order.status = "SHIPPED"
john_order.status = "COMPLETED"