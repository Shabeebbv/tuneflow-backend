from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class AuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="1234",
            name="Test User"
        )
        self.user.is_active = True
        self.user.status = "active"
        self.user.save()

    #  REGISTER TEST
    def test_register(self):
        response = self.client.post("/api/register/", {
            "email": "new@gmail.com",
            "password": "1234",
            "name": "New User"
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)

    #  LOGIN SUCCESS
    def test_login_success(self):
        response = self.client.post("/api/login/", {
            "email": "test@gmail.com",
            "password": "1234"
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    #  LOGIN FAIL
    def test_login_fail(self):
        response = self.client.post("/api/login/", {
            "email": "test@gmail.com",
            "password": "wrong"
        }, format='json')

        self.assertEqual(response.status_code, 400)

    #  LOGIN NOT VERIFIED
    def test_login_not_verified(self):
        user = User.objects.create_user(
            email="inactive@gmail.com",
            password="1234",
            name="Inactive User"
        )
        user.is_active = False
        user.save()

        response = self.client.post("/api/login/", {
            "email": "inactive@gmail.com",
            "password": "1234"
        }, format='json')

        self.assertEqual(response.status_code, 403)

    #  VERIFY EMAIL
    def test_verify_email(self):
        user = User.objects.create_user(
            email="verify@gmail.com",
            password="1234",
            name="Verify User"
        )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        response = self.client.get(f"/api/verify/{uid}/{token}/")

        self.assertEqual(response.status_code, 200)

    #  VERIFY EMAIL INVALID
    def test_verify_invalid(self):
        response = self.client.get("/api/verify/invalid/token/")

        self.assertEqual(response.status_code, 400)

    #  FORGOT PASSWORD
    def test_forgot_password(self):
        response = self.client.post("/api/forgot-password/", {
            "email": "test@gmail.com"
        }, format='json')

        self.assertEqual(response.status_code, 200)

    #  FORGOT PASSWORD USER NOT FOUND
    def test_forgot_password_fail(self):
        response = self.client.post("/api/forgot-password/", {
            "email": "unknown@gmail.com"
        }, format='json')

        self.assertEqual(response.status_code, 404)

    #  RESET PASSWORD
    def test_reset_password(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        response = self.client.post(f"/api/reset/{uid}/{token}/", {
            "password": "newpass123"
        }, format='json')

        self.assertEqual(response.status_code, 200)

    #  RESET PASSWORD INVALID TOKEN
    def test_reset_password_invalid(self):
        response = self.client.post("/api/reset/invalid/token/", {
            "password": "1234"
        }, format='json')

        self.assertEqual(response.status_code, 400)