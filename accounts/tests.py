from django.urls import reverse, resolve
from django.test import TestCase
from .models import CustomUser
from django.contrib.auth import get_user_model



class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="aditya", email="aditya@email.com", password="testpass123")
        self.assertEqual(user.username, "aditya")
        self.assertEqual(user.email, "aditya@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(username="aditya", email="aditya@email.com", password="testpass123")
        self.assertEqual(user.username, "aditya")
        self.assertEqual(user.email, "aditya@email.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class SignUpTests(TestCase):
    username = "newuser"
    email = "newuser@email.com"
    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "False Sign Up!!!")

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)                                                
        self.assertEqual(new_user.username, self.username)                                                
        self.assertEqual(new_user.email, self.email)                                                


    # def test_signup_view(self):
    #     view = resolve("/accounts/signup/")
    #     self.assertEqual(view.func.__name__, SignUpView.as_view().__name__)
