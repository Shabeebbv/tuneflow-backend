from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from products.models import Product
from cart.models import CartItem
from .models import Order, OrderItem

User = get_user_model()


class OrderTests(TestCase):

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

    #  CREATE ORDER SUCCESS
def test_create_order_success(self):
    CartItem.objects.create(
        user=self.user,
        product=self.product,
        quantity=2
    )

    response = self.client.post("/api/orders/create/", {
        "name": "Shabeeb",
        "email": "test@gmail.com",
        "phone": "1234567890",
        "address": "Test address",
        "city": "Kochi",
        "pincode": "683542",
        "landmark": "Near school",
        "payment_method": "COD"
    }, format='json')

    print(response.data)  # optional debug

    self.assertEqual(response.status_code, 201)
    self.assertEqual(Order.objects.count(), 1)
    self.assertEqual(OrderItem.objects.count(), 1)

        # cart should be cleared
    self.assertEqual(CartItem.objects.count(), 0)

    #  CREATE ORDER WITH EMPTY CART
    def test_create_order_empty_cart(self):
        response = self.client.post("/api/orders/create/", {
            "name": "Shabeeb",
            "address": "Test address",
            "phone": "1234567890"
        }, format='json')

        self.assertEqual(response.status_code, 400)

    #  INVALID DATA
    def test_create_order_invalid_data(self):
        CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

        response = self.client.post("/api/orders/create/", {
            "name": "",   # invalid
        }, format='json')

        self.assertEqual(response.status_code, 400)

    #  GET USER ORDERS
    def test_get_user_orders(self):
        order = Order.objects.create(
            user=self.user,
            name="Shabeeb",
            address="Test address",
            phone="1234567890"
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price=100,
            old_price=120
        )

        response = self.client.get("/api/orders/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    #  UNAUTHORIZED ACCESS
    def test_orders_requires_auth(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/orders/")

        self.assertEqual(response.status_code, 401)