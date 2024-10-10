from django.test import TestCase
from django.urls import reverse
from store.models import Product
from .cart import Cart


class CartAddViewTest(TestCase):
    def setUp(self):
        # Crear un producto de prueba
        self.product = Product.objects.create(title="Producto Test", price=10.0)

    """    

    def test_cart_add_post(self):
        response = self.client.post(
            reverse("cart_add"),
            {"action": "post", "product_id": self.product.id, "product_quantity": 2},
        )

        # Verificar que la respuesta es JSON y que el código de estado es 200
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"Usted pidío:": self.product.title, " con un total de:": 2},
        )

    def test_cart_add_invalid_product_id(self):
        response = self.client.post(
            reverse("cart_add"),
            {
                "action": "post",
                "product_id": 999,  # ID que no existe
                "product_quantity": 2,
            },
        )

        # Verificar que se retorna un error 404
        self.assertEqual(response.status_code, 404)

    def test_cart_add_invalid_quantity(self):
        response = self.client.post(
            reverse("cart_add"),
            {
                "action": "post",
                "product_id": self.product.id,
                "product_quantity": "invalid",  # Cantidad no válida
            },
        )

        # Verificar que se retorna un error 400
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content, {"error": "Cantidad o ID del producto no válidos."}
        )

    def test_cart_add_method_not_allowed(self):
        response = self.client.get(reverse("cart_add"))  # Usar GET en lugar de POST

        # Verificar que se retorna un error 405
        self.assertEqual(response.status_code, 405)

        """
