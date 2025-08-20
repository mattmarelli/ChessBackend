import pytest

from django.test import TestCase

from chessbackend.models import User
from chessbackend.factories import UserFactory
from endpoints.tests.mixins.endpoint_test_mixin import EndpointTestMixin

class LoginTests(EndpointTestMixin, TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@email.com", password="test_password", username="test_user"
        )

    def test_login_endpoint(self):
        response = self.client.post("/login/", data={})

        print(f"RESPONSE: {response}")
        print(f"RESPONSE DATA: {response.data}")

        response_data = response.data
        assert response_data["detail"] == "Email or password missing!"

        print(f"USER EMAIL: {self.user.email}")
        print(f"USER PASSWORD: {self.user.password}")
        response_2 = self.client.post("/login/", data={"email":self.user.email, "password":"test_password"})

        print(f"RESPONSE: {response_2}")
        print(f"RESPONSE DATA: {response_2.data}")
