import products


class Product:
    """Represents a product in a store with a name, price, and quantity."""

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a Product instance.

        Args:
            name (str): The name of the product.
            price (float): The price per unit of the product.
            quantity (int): The quantity of the product in stock.

        Raises:
            ValueError: If name is empty or if price/quantity are negative.
        """
        if not name or price < 0 or quantity < 0:
            raise ValueError(
                "Invalid input: name cannot be empty, and price/quantity must be non-negative."
            )

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> float:
        """Returns the current quantity of the product in stock."""
        return self.quantity

    def set_quantity(self, quantity: int):
        """
        Sets the quantity of the product. Deactivates the product if quantity is 0.

        Args:
            quantity (int): The new quantity to set.

        Raises:
            ValueError: If the quantity is negative.
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Returns True if the product is active, otherwise False."""
        return self.active

    def activate(self):
        """Activates the product, making it available for purchase."""
        self.active = True

    def deactivate(self):
        """Deactivates the product, making it unavailable for purchase."""
        self.active = False

    def show(self) -> str:
        """Returns a string representing the product details."""
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        """
        Buys a given quantity of the product and returns the total price.

        Args:
            quantity (int): The quantity to purchase.

        Returns:
            float: The total price for the purchased quantity.

        Raises:
            ValueError: If quantity is non-positive.
            Exception: If the product is inactive or if requested quantity is unavailable.
        """
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")
        if not self.is_active():
            raise Exception("Product is inactive and cannot be purchased.")
        if quantity > self.quantity:
            raise Exception("Insufficient quantity in stock.")

        total_price = quantity * self.price
        self.set_quantity(self.quantity - quantity)
        return total_price

class NonStockedProduct(Product):
    """Represents a non-stocked product with no quantity tracking (e.g., software licenses)."""

    def __init__(self, name: str, price: float):
        """Initializes a NonStockedProduct with zero quantity."""
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int):
        """Prevents change in quantity for non-stocked products."""
        raise Exception("Quantity cannot be set for non-stocked products.")

    def show(self) -> str:
        """Returns a string representing  non-stocked product details """
        return f"{self.name}, Price: ${self.price}, Non-stocked product"
class LimitedProduct(Product):
    """Represents a product that can be purchased a limited number of times per order (e.g., shipping fees)."""

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """
        Initializes a LimitedProduct with a maximum purchase limit per order.

        Args:
            maximum (int): The maximum quantity allowed per purchase.
        """
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        """Ensures that the purchase quantity does not exceed the set maximum."""
        if quantity > self.maximum:
            raise Exception(f"Cannot buy more than {self.maximum} of {self.name} in a single order.")
        return super().buy(quantity)
    def show(self) -> str:
        """Returns a stirng by representing limited product details."""
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Max per order{self.maximum}"






# Testing code (commented out to avoid unused variable warning)
# Setup initial stock of inventory
import store

# setup initial stock of inventory
product_list = [ products.Product("MacBook Air M2", price=1450, quantity=100),
                 products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                 products.Product("Google Pixel 7", price=500, quantity=250),
                 products.NonStockedProduct("Windows License", price=125),
                 products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
               ]
best_buy = store.Store(product_list)

