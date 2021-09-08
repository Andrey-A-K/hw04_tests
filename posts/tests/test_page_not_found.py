from django.test import Client, TestCase


class PostURLTests(TestCase):
    @classmethod
    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()

    def test_page(self):
        """страница не найдена возвращает код 404"""
        response = self.guest_client.get('/test_page/')
        self.assertEqual(response.status_code, 404)
