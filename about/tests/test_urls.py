from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AboutURLTests(TestCase):
    @classmethod
    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()

    def test_urls_uses_correct_template(self):
        """Соответствие страниц шаблонам"""
        templates_url_names = {
            'about/author.html': 'about:author',
            'about/tech.html': 'about:tech',
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.guest_client.get(reverse(reverse_name))
                self.assertTemplateUsed(response, template)

    def test_page_available_everyone(self):
        """Страница  доступна всем"""
        response_code_page = {
            'about:author': 200,
            'about:tech': 200,
        }
        for template, stat_cod in response_code_page.items():
            with self.subTest():
                response = self.guest_client.get(reverse(template))
                self.assertEqual(response.status_code, stat_cod)
