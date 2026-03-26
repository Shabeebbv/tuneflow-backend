from django.test import TestCase
from rest_framework.test import APIClient
from .models import Product


class ProductTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # create products
        self.product1 = Product.objects.create(
            name="iPhone",
            category="Apple",
            description="Smartphone",
            price=1000,
            old_price=1200
        )

        self.product2 = Product.objects.create(
            name="Galaxy",
            category="Samsung",
            description="Android phone",
            price=800,old_price=1200
        )

        self.product3 = Product.objects.create(
            name="AirPods",
            category="Apple",
            description="Wireless earbuds",
            price=200,old_price=1200
        )

    #  GET ALL PRODUCTS
    def test_product_list(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    #  SEARCH PRODUCTS
    def test_search_products(self):
        response = self.client.get("/api/products/?search=iphone")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    #  FILTER BY BRAND
    def test_filter_by_brand(self):
        response = self.client.get("/api/products/?brand=Apple")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    #  FILTER BY MIN PRICE
    def test_filter_min_price(self):
        response = self.client.get("/api/products/?min_price=900")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    #  FILTER BY MAX PRICE
    def test_filter_max_price(self):
        response = self.client.get("/api/products/?max_price=300")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    #  FILTER PRICE RANGE
    def test_filter_price_range(self):
        response = self.client.get("/api/products/?min_price=500&max_price=1000")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    #  PAGINATION
    def test_pagination(self):
        # create extra products to exceed page size
        for i in range(15):
            Product.objects.create(
                name=f"Product {i}",
                category="Test",
                description="Test",
                price=100,
                old_price=1200
            )

        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 10)  # page_size = 10

    #  PRODUCT DETAIL
    def test_product_detail(self):
        response = self.client.get(f"/api/products/{self.product1.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "iPhone")

    #  PRODUCT NOT FOUND
    def test_product_not_found(self):
        response = self.client.get("/api/products/999/")

        self.assertEqual(response.status_code, 404)  # ⚠️ your view returns 200
        self.assertIn("Error", response.data)