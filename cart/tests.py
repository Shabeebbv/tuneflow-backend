from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from products.models import Product
from .models import CartItem

User = get_user_model()


class CartTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="Test@1234",
            name="Test User"
        )
        self.user.is_active = True
        self.user.status = "active"
        self.user.save()

        # authenticate user
        self.client.force_authenticate(user=self.user)

        # create product
        self.product = Product.objects.create(
            name="Test Product",
            price=100
        )

    #  ADD TO CART
    def test_add_to_cart(self):
        response = self.client.post("/cart/add/", {
            "product_id": self.product.id
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)

    #  ADD SAME PRODUCT AGAIN (quantity increase)
    def test_add_same_product(self):
        self.client.post("/cart/add/", {"product_id": self.product.id}, format='json')
        self.client.post("/cart/add/", {"product_id": self.product.id}, format='json')

        cart_item = CartItem.objects.get(user=self.user, product=self.product)

        self.assertEqual(cart_item.quantity, 2)

    #  ADD INVALID PRODUCT
    def test_add_invalid_product(self):
        response = self.client.post("/cart/add/", {
            "product_id": 999
        }, format='json')

        self.assertEqual(response.status_code, 404)

    #  VIEW CART
    def test_view_cart(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)

        response = self.client.get("/cart/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    #  REMOVE FROM CART
    def test_remove_from_cart(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)

        response = self.client.post("/cart/remove/", {
            "product_id": self.product.id
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 0)

    #  UPDATE CART (increase)
    def test_update_cart_increase(self):
        cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=1)

        response = self.client.post("/cart/update/", {
            "product_id": self.product.id,
            "action": "increase"
        }, format='json')

        cart_item.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart_item.quantity, 2)

    #  UPDATE CART (decrease)
    def test_update_cart_decrease(self):
        cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=3)

        response = self.client.post("/cart/update/", {
            "product_id": self.product.id,
            "action": "decrease"
        }, format='json')

        cart_item.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart_item.quantity, 2)

    #  UPDATE NON-EXISTING ITEM
    def test_update_cart_not_found(self):
        response = self.client.post("/cart/update/", {
            "product_id": 999,
            "action": "increase"
        }, format='json')

        self.assertEqual(response.status_code, 404)

    #  UNAUTHORIZED ACCESS
    def test_cart_requires_auth(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/cart/")

        self.assertEqual(response.status_code, 401)