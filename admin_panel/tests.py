from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from products.models import Product
from orders.models import Order

User = get_user_model()


class AdminTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # ✅ create admin user
        self.admin = User.objects.create_user(
            email="admin@gmail.com",
            password="Admin@123",
            name="Admin"
        )
        self.admin.role = "admin"
        self.admin.is_active = True
        self.admin.save()

        # authenticate admin
        self.client.force_authenticate(user=self.admin)

        # create normal user
        self.user = User.objects.create_user(
            email="user@gmail.com",
            password="User@123",
            name="User"
        )
        self.user.status = "active"
        self.user.save()

        # create product
        self.product = Product.objects.create(
            name="Test Product",
            category="Test",
            description="Test",
            price=100,
            old_price=120,
            rating=4.5
        )

    #  ADMIN LOGIN
    def test_admin_login(self):
        self.client.force_authenticate(user=None)

        response = self.client.post("/api/admin/login/", {
            "email": "admin@gmail.com",
            "password": "Admin@123"
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    #  GET USERS
    def test_user_list(self):
        response = self.client.get("/api/admin/users/")
        self.assertEqual(response.status_code, 200)

    #  USER DETAIL
    def test_user_detail(self):
        response = self.client.get(f"/api/admin/users/{self.user.id}/")
        self.assertEqual(response.status_code, 200)

    #  TOGGLE USER STATUS
    def test_toggle_user_status(self):
        response = self.client.patch(f"/api/admin/users/{self.user.id}/toggle-status/")
        self.assertEqual(response.status_code, 200)

    #  DELETE USER
    def test_delete_user(self):
        response = self.client.delete(f"/api/admin/users/{self.user.id}/delete/")
        self.assertEqual(response.status_code, 200)

    #  RESTORE USER
    def test_restore_user(self):
        self.user.is_deleted = True
        self.user.save()

        response = self.client.patch(f"/api/admin/users/{self.user.id}/restore/")
        self.assertEqual(response.status_code, 200)

    #  CREATE PRODUCT
    def test_create_product(self):
        response = self.client.post("/api/admin/products/", {
            "name": "New Product",
            "category": "Test",
            "description": "Desc",
            "price": 200,
            "old_price": 250,
            "rating": 4.0
        }, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    #  GET PRODUCTS
    def test_get_products(self):
        response = self.client.get("/api/admin/products/")
        self.assertEqual(response.status_code, 200)

    #  UPDATE PRODUCT
    def test_update_product(self):
        response = self.client.put(f"/api/admin/products/{self.product.id}/", {
            "name": "Updated",
            "category": "Test",
            "description": "Updated",
            "price": 150,
            "old_price": 200,
            "rating": 4.2
        }, format='json')

        self.assertEqual(response.status_code, 200)

    # ❌ DELETE PRODUCT
    def test_delete_product(self):
        response = self.client.delete(f"/api/admin/products/{self.product.id}/delete/")
        self.assertEqual(response.status_code, 200)

    # 📦 ORDER LIST
    def test_order_list(self):
        Order.objects.create(
            user=self.user,
            name="Test",
            phone="123",
            address="Addr",
            city="City",
            pincode="123",
            landmark="Near",
            payment_method="COD"
        )

        response = self.client.get("/api/admin/orders/")
        self.assertEqual(response.status_code, 200)

    #  UPDATE ORDER STATUS
    def test_update_order_status(self):
        order = Order.objects.create(
            user=self.user,
            name="Test",
            phone="123",
            address="Addr",
            city="City",
            pincode="123",
            landmark="Near",
            payment_method="COD"
        )
        response = self.client.patch(f"/api/admin/orders/{order.id}/status/", {
            "status": "shipped"
        }, format='json')

        self.assertEqual(response.status_code, 200)

    #  REVENUE
    # def test_revenue(self):
    #     response = self.client.get("/api/admin/revenue/")
    #     self.assertEqual(response.status_code, 200)

    # 📊 ORDER COUNT
    def test_order_count(self):
        response = self.client.get("/api/admin/orders/count/")
        self.assertEqual(response.status_code, 200)

    # 📊 CATEGORY STATS
    def test_orders_by_category(self):
        response = self.client.get("/api/admin/orders-by-category/")
        self.assertEqual(response.status_code, 200)

    # 📈 MONTHLY SALES
    def test_monthly_sales(self):
        response = self.client.get("/api/admin/monthly-sales/")
        self.assertEqual(response.status_code, 200)