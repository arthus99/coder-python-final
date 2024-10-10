from django.test import TestCase
from django.urls import reverse
from .models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronicos", slug="electronicos"
        )

    def test_str_method(self):
        self.assertEqual(str(self.category), "Electronicos")

    def test_get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), "/search/electronicos")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronicos", slug="electronicos"
        )
        self.product = Product.objects.create(
            Category=self.category,
            title="Smartphone",
            brand="Galaxy",
            description="ultimo modelo de smartphone",
            slug="smartphone",
            price=299.99,
            image="testimages/galaxy.jpg",
        )

    def test_str_method(self):
        self.assertEqual(str(self.product), "Smartphone")

    def test_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), "/product/smartphone")


# Pruebas para las vistas


class StoreViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronicos", slug="electronicos"
        )
        self.product = Product.objects.create(
            Category=self.category,
            title="Smartphone",
            brand="Galaxy",
            description="ultimo modelo de smartphone",
            slug="smartphone",
            price=299.99,
            image="testimages/galaxy.jpg",
        )

    def test_store_view(self):
        response = self.client.get(reverse("store"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "store/store.html")
        self.assertContains(response, "Smartphone")


class CategoriesViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronicos", slug="electronicos"
        )

    def test_categories_view(self):
        self.assertTrue(bool(self.category), "El diccionario está vacío")


class ListCategoryViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronicos", slug="electronicos"
        )
        self.product1 = Product.objects.create(
            Category=self.category,
            title="Smartphone",
            brand="Galaxy",
            description="ultimo modelo de smartphone",
            slug="smartphone",
            price=299.99,
            image="testimages/galaxy.jpg",
        )
        self.product2 = Product.objects.create(
            Category=self.category,
            title="Laptop",
            brand="BrandY",
            description="Laptop de alto rendimiento",
            slug="laptop",
            price=799.99,
            image="testimages/laptop.jpg",
        )

    def test_list_category_view(self):
        response = self.client.get(reverse("list_category", args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "store/list-category.html")
        self.assertContains(response, "Electronicos")
        self.assertContains(response, "Smartphone")
        self.assertContains(response, "Laptop")


class ProductInfoViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronicos", slug="electronicos"
        )
        self.product = Product.objects.create(
            Category=self.category,
            title="Smartphone",
            brand="Galaxy",
            description="Último modelo de smartphone",
            slug="smartphone",
            price=299.99,
            image="testimages/galaxy.jpg",
        )

    def test_product_info_view(self):
        response = self.client.get(reverse("product_info", args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "store/product-info.html")
        self.assertContains(response, "Smartphone")
        self.assertContains(response, "Último modelo de smartphone")
