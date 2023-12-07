from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

UserModel = get_user_model()


class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

    def test_password_reset_success(self):
        url = reverse("password_reset")
        data = {"email": "testuser@example.com"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Password reset e-mail has been sent.")

    def test_password_reset_failure_invalid_email(self):
        url = reverse("password_reset")
        data = {"email": "invalid_email@example.com"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)  # Check for specific error messages

    def test_password_reset_failure_no_authentication(self):
        url = reverse("password_reset")
        data = {"email": "testuser@example.com"}
        self.client.force_authenticate(user=None)  # Simulate unauthenticated user
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Password reset e-mail has been sent.")


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post("/auth/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_unauthenticated(self):
        response = self.client.post("/auth/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
