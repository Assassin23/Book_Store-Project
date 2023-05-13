from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from .models import Book, Review

# Create your tests here.
class BookTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reviewuser",
            email="reviewuser@email.com",
            password="testpass123"
        )
        cls.special_permission = Permission.objects.get(codename="special_status")
        cls.book = Book.objects.create(
            title="Harry Potter and The Half-Blood Prince",
            author="J. K. Rowling",
            price=599.00
        )
        cls.review = Review.objects.create(
            book=cls.book,
            author = cls.user,
            review="An excellent review."
        )
    
    def test_book_listing(self):
        self.assertEqual(self.book.title, "Harry Potter and The Half-Blood Prince")
        self.assertEqual(self.book.author, "J. K. Rowling")
        self.assertEqual(self.book.price, 599.00)
    
    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        resp = self.client.get(reverse("book_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Harry Potter")
        self.assertTemplateUsed(resp, "books/book_list.html")
    
    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()
        resp = self.client.get(reverse("book_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(
        resp, "%s?next=/books/" % (reverse("account_login")))
        response = self.client.get(
        "%s?next=/books/" % (reverse("account_login")))
        self.assertContains(response, "Log In")
        self.assertTemplateUsed(response, "account/login.html")
    
    def test_book_detail_view(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        self.user.user_permissions.add(self.special_permission)
        resp = self.client.get(self.book.get_absolute_url())
        no_resp = self.client.get("/books/12345/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(no_resp.status_code, 404)
        self.assertContains(resp, "Harry Potter")
        self.assertContains(resp, "An excellent review.")
        self.assertTemplateUsed(resp, "books/book_detail.html")

