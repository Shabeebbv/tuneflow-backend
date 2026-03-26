from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from products.models import Product
from .models import Wishlist

User = get_user_model()


class WishlistTests(TestCase):

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
            category="Test",
            description="Test desc",
            price=100,
            old_price=120
        )

    # ✅ ADD TO WISHLIST
    def test_add_to_wishlist(self):
        response = self.client.post("/api/wishlist/add/", {
            "product_id": self.product.id
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Wishlist.objects.count(), 1)

    # ✅ ADD SAME PRODUCT (no duplicate)
    def test_add_duplicate(self):
        self.client.post("/api/wishlist/add/", {"product_id": self.product.id}, format='json')
        self.client.post("/api/wishlist/add/", {"product_id": self.product.id}, format='json')

        self.assertEqual(Wishlist.objects.count(), 1)  # get_or_create prevents duplicate

    # ❌ ADD INVALID PRODUCT
    def test_add_invalid_product(self):
        response = self.client.post("/api/wishlist/add/", {
            "product_id": 999
        }, format='json')

        self.assertEqual(response.status_code, 404)

    # ✅ VIEW WISHLIST
    def test_view_wishlist(self):
        Wishlist.objects.create(user=self.user, product=self.product)

        response = self.client.get("/api/wishlist/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    # ✅ REMOVE FROM WISHLIST
    def test_remove_wishlist(self):
        Wishlist.objects.create(user=self.user, product=self.product)

        response = self.client.post("/api/wishlist/remove/", {
            "product_id": self.product.id
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Wishlist.objects.count(), 0)

    # ❌ REMOVE NON-EXISTING ITEM
    def test_remove_non_existing(self):
        response = self.client.post("/api/wishlist/remove/", {
            "product_id": 999
        }, format='json')

        self.assertEqual(response.status_code, 200)  # your API still returns 200

    # 🔒 UNAUTHORIZED ACCESS
    def test_requires_auth(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/wishlist/")

        self.assertEqual(response.status_code, 401)