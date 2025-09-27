"""Stateful simulator for the Sauce Demo storefront used in tests."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    price: float


class SauceSimulator:
    def __init__(self) -> None:
        self._inventory: list[Product] = [
            Product("Sauce Labs Backpack", 29.99),
            Product("Sauce Labs Bike Light", 9.99),
            Product("Sauce Labs Bolt T-Shirt", 15.99),
            Product("Sauce Labs Fleece Jacket", 49.99),
            Product("Sauce Labs Onesie", 7.99),
            Product("Test.allTheThings() T-Shirt (Red)", 15.99),
        ]
        self.reset()

    def reset(self) -> None:
        self.cart: list[Product] = []
        self.sorted_products: list[Product] = list(self._inventory)
        self.logged_in = False
        self.checkout_message = ""
        self.error_message = ""

    def attempt_login(self, username: str, password: str) -> bool:
        """Validate credentials and update simulator state."""

        valid_credentials = {
            "standard_user": "secret_sauce",
        }

        if valid_credentials.get(username) == password:
            self.logged_in = True
            self.error_message = ""
            return True

        self.logged_in = False
        self.error_message = (
            "Epic sadface: Username and password do not match any user in this service"
        )
        return False

    def sort_by(self, option_text: str) -> None:
        if option_text.lower().startswith("price"):
            self.sorted_products = sorted(self._inventory, key=lambda product: product.price)
        else:
            self.sorted_products = list(self._inventory)

    def add_item(self, index: int) -> Product:
        product = self.sorted_products[index]
        self.cart.append(product)
        return product

    def cart_badge(self) -> str:
        return str(len(self.cart))

    def cart_names(self) -> list[str]:
        return [product.name for product in self.cart]

    def checkout(self) -> str:
        self.checkout_message = "Order dispatched successfully"
        self.cart.clear()
        return self.checkout_message
