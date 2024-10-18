from decimal import Decimal
from store.models import Product
from .models import CartModel
import copy


class Cart:
    def __init__(self, request):
        self.session = request.session
        # Regresa la sesión del usuario
        self.cart = self.session.get("my_session", {})
        if not isinstance(self.cart, dict):
            self.cart = {}

        self.session["my_session"] = self.cart

    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["qty"] = product_qty  # Actualizo la cantidad
        else:
            self.cart[product_id] = {"price": str(product.price), "qty": product_qty}

        # request.session.modified = True
        self.session.modified = True

    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())

    def __iter__(self):
        all_products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_products_ids)
        # cart = self.cart.copy()
        # import copy

        cart = copy.deepcopy(self.cart)

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total"] = item["price"] * item["qty"]
            yield item

    def get_total(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.cart.values())

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]  # Borra el item del dicc
            self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)
        # product_quantity = qty
        if product_id in self.cart and qty > 0:
            self.cart[product_id]["qty"] = qty
        elif product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def get_cart_from_db(self, user):
        cart_model, created = CartModel.objects.get_or_create(user=user)
        self.cart = (
            cart_model.cart_data if isinstance(cart_model.cart_data, dict) else {}
        )
        self.session["my_session"] = self.cart

    def save_cart_to_db(self, user):
        CartModel.objects.update_or_create(user=user, defaults={"cart_data": self.cart})
