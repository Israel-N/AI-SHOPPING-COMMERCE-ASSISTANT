class OrderManager:

    def __init__(self):
        self.cart = []

    def add_to_cart(self, product_name, quantity=1):

        self.cart.append({
            "product": product_name,
            "quantity": quantity
        })

        return f"{quantity} {product_name}(s) added to cart."

    def view_cart(self):

        if not self.cart:
            return "Your cart is empty."

        result = "Cart:\n"

        for item in self.cart:
            result += (
                f"{item['product']} "
                f"x {item['quantity']}\n"
            )

        return result

    def checkout(self):

        if not self.cart:
            return "Cart is empty."

        total_items = len(self.cart)

        self.cart.clear()

        return (
            f"Order placed successfully. "
            f"{total_items} item(s) purchased."
        )