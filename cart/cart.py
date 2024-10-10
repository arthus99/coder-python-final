class Cart:
    def __init__(self, request):
        self.session = request.session
        # Regresa la sesión del usuario
        cart = self.session.get("my_session")
        # de no existir genera una nueva sesión
        if "my_session" not in request.session:
            cart = self.session["my_session"] = {}

        self.cart = cart

    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["qty"] = product_qty  # Actualizo la cantidad
        else:
            self.cart[product_id] = {"price": str(product.price), "qty": product_qty}

        self.session.modified = True
