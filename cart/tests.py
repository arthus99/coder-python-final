from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from store.models import Product, Category
from .cart import Cart


class CartTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Crea una Categoria de prueba
        self.category = Category.objects.create(
            name="Electronicos", slug="electronicos"
        )
        # Crear un producto de prueba
        self.product = Product.objects.create(
            Category=self.category,
            title="Smartphone",
            brand="Galaxy",
            description="Último modelo de smartphone",
            slug="smartphone",
            price=299.99,
            image="testimages/galaxy.jpg",
        )

        # Crear una solicitud para simular la sesión
        self.request = self.factory.get("/")

        # Inicializa el middleware de sesión
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(self.request)
        self.request.session.save()  # Esto inicializa la sesión

        # Inicializar el carrito con la solicitud
        self.cart = Cart(self.request)

    def test_cart_initialization(self):
        # Verifica que el carrito esté inicializado correctamente
        self.assertEqual(self.cart.cart, {})

    def test_add_product(self):
        # Agregar un producto al carrito
        self.cart.add(self.product, 1)
        self.assertEqual(
            len(self.cart.cart), 1
        )  # Verifica que el carrito tenga un producto
        self.assertEqual(
            self.cart.cart[str(self.product.id)],
            {"price": str(self.product.price), "qty": 1},
        )

    def test_add_product_quantity(self):
        # Agregar el mismo producto con una cantidad diferente
        self.cart.add(self.product, 2)
        self.assertEqual(
            self.cart.cart[str(self.product.id)]["qty"], 2
        )  # Verifica que la cantidad se actualice

    def test_session_modified(self):
        # Verifica que la sesión se marque como modificada al agregar un producto
        self.cart.add(self.product, 1)
        self.assertTrue(
            self.request.session.modified
        )  # La sesión debe estar marcada como modificada

    def test_delete_product(self):
        self.assertEqual(self.cart.cart, {})  # verifico que el carrito este vacio
        self.cart.add(self.product, 2)  # agregamos un producto
        self.assertEqual(
            len(self.cart.cart), 1
        )  # Verifica que el carrito tenga un producto
        self.cart.delete(self.product.id)
        self.assertEqual(self.cart.cart, {})  # verifico que el carrito este vacio

    def test_update_product(self):
        self.cart.add(self.product, 2)  # agregamos un producto
        self.assertEqual(
            self.cart.cart[str(self.product.id)]["qty"], 2
        )  # Verifica que sea la cantidad
        self.cart.update(self.product.id, 3)
        self.assertEqual(self.cart.cart[str(self.product.id)]["qty"], 3)


class CartAddViewTest(TestCase):
    def setUp(self):
        # Crea una Categoria de prueba
        self.category = Category.objects.create(
            name="Electronicos", slug="electronicos"
        )
        # Crear un producto de prueba
        self.product = Product.objects.create(title="Producto Test", price=10.0)

    def test_cart_add_post(self):
        response = self.client.post(
            reverse("cart-add"),
            {"action": "post", "product_id": self.product.id, "product_quantity": 2},
        )

        # Verificar que la respuesta es JSON y que el código de estado es 200
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"qty": 2},
        )

    def test_cart_add_invalid_product_id(self):
        response = self.client.post(
            reverse("cart-add"),
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
            reverse("cart-add"),
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
        response = self.client.get(reverse("cart-add"))  # Usar GET en lugar de POST

        # Verificar que se retorna un error 405
        self.assertEqual(response.status_code, 405)
