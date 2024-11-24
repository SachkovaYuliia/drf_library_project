from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test_password')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin_password')

        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'test_password'
        })
        self.access_token = response.data['access']

        admin_response = self.client.post('/api/token/', {
            'username': 'admin',
            'password': 'admin_password'
        })
        self.admin_access_token = admin_response.data['access']

        self.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            genre="Genre One",
            publication_year=2020
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            genre="Genre Two",
            publication_year=2021
        )

    def test_get_books(self):
        """Тест для перевірки списку книг"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_book_authenticated(self):
        """Тест для створення книги автентифікованим користувачем"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {
            "title": "Book Three",
            "author": "Author Three",
            "genre": "Genre Three",
            "publication_year": 2022
        }
        response = self.client.post('/api/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Тест для створення книги неавтентифікованим користувачем"""
        self.client.credentials()  
        data = {
            "title": "Book Four",
            "author": "Author Four",
            "genre": "Genre Four",
            "publication_year": 2023
        }
        response = self.client.post('/api/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book(self):
        """Тест для оновлення книги"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {
            "title": "Updated Book One",
            "author": "Updated Author One",
            "genre": "Updated Genre One",
            "publication_year": 2020
        }
        response = self.client.put(f'/api/books/{self.book1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book One")

    def test_delete_book_admin(self):
        """Тест для видалення книги адміністратором"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}')
        response = self.client.delete(f'/api/books/{self.book2.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_non_admin(self):
        """Тест для видалення книги неадміністратором"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(f'/api/books/{self.book2.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
