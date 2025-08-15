from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models import Book, Author


class BookAPITests(APITestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()

        # Create author
        self.author = Author.objects.create(name="Author One")

        # Create a book
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publication_year=2022
        )

        # API URLs
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book.id])
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", args=[self.book.id])
        self.delete_url = reverse("book-delete", args=[self.book.id])

    # -------------------- LIST --------------------
    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Book", str(response.data))

    # -------------------- RETRIEVE --------------------
    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")

    # -------------------- CREATE --------------------
    def test_create_book_requires_authentication(self):
        data = {
            "title": "New Book",
            "author": self.author.id,  # must use ID for FK
            "publication_year": 2021,
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        data = {
            "title": "New Book",
            "author": self.author.id,
            "publication_year": 2021,
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    # -------------------- UPDATE --------------------
    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        data = {"title": "Updated Title", "author": self.author.id, "publication_year": 2025}
        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    # -------------------- DELETE --------------------
    def test_delete_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # -------------------- FILTERING --------------------
    def test_filter_books_by_title(self):
        response = self.client.get(self.list_url + "?title=Test Book")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_books_by_publication_year(self):
        response = self.client.get(self.list_url + "?publication_year=2022")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_books_by_author_name(self):
        response = self.client.get(self.list_url + "?author__name=Author One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # -------------------- SEARCH --------------------
    def test_search_books(self):
        response = self.client.get(self.list_url + "?search=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # -------------------- ORDERING --------------------
    def test_order_books_by_title(self):
        Book.objects.create(title="Another Book", author=self.author, publication_year=2020)
        response = self.client.get(self.list_url + "?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))

