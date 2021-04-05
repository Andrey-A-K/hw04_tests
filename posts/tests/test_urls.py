from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем пользователя
        cls.user = User.objects.create_user(username='AA')
        cls.user_2 = User.objects.create_user(username='BB')
        # Создаем группу
        cls.test_group = Group.objects.create(title='leo', slug='leo')
        # Создадим запись в БД для проверки доступности
        # адреса group/leo/
        Post.objects.create(
            text='Тестовый текст для теста',
            pub_date=Post.pub_date,
            author=cls.user,
            group=cls.test_group
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем второй клиент
        self.authorized_client = Client()
        self.authorized_client_2 = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)
        self.authorized_client_2.force_login(self.user_2)

    def test_the_home_page_is_available_to_everyone(self):
        """Главноая страница доступна всем"""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_the_group_page_is_available_to_everyone(self):
        """Страница group/leo/ доступна всем"""
        response = self.guest_client.get('/group/leo/')
        self.assertEqual(response.status_code, 200)

    def test_the_author_page_is_available_to_everyone(self):
        """Страница /about/author/ доступна всем"""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_the_technology_page_is_available_to_everyone(self):
        """Страница /about/tech/ доступна всем"""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)

    def test_the_profile_page_is_available_to_everyone(self):
        """Страница /username/ доступна всем"""
        response = self.guest_client.get('/AA/')
        self.assertEqual(response.status_code, 200)

    def test_the_page_of_a_separate_post_is_available_to_everyone(self):
        """Страница отдельного поста доступна всем"""
        response = self.guest_client.get('/AA/1/')
        self.assertEqual(response.status_code, 200)

    def test_new_list_url_exists_at_desired_location(self):
        """Страница /new/ доступна авторизованному пользователю"""
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_the_edit_page_is_available_to_the_not_authorized_user(self):
        """Страница редактирования недоступна не автору поста"""
        response = self.authorized_client_2.get('/AA/1/edit/')
        self.assertEqual(response.status_code, 302)

    def test_the_edit_page_is_available_to_the_authorized_user(self):
        """Страница редактирования доступна автору поста"""
        response = self.authorized_client.get('/AA/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_from_the_edit_page(self):
        """редирект анонима со страницы редактирования"""
        response = self.guest_client.get('/AA/1/edit/')
        self.assertEqual(response.status_code, 302)

    def test_correct_redirect_of_the_edit_page_without_access_rights(self):
        """правильный редирект страницы редактирования без прав доступа"""
        response = self.guest_client.get('/AA/1/edit/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/AA/1/edit/')

    def test_new_list_url_redirect_anonymous(self):
        """Страница /new/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get('/new/')
        self.assertEqual(response.status_code, 302)

    def test_urls_uses_correct_template(self):
        """Соответствие страниц шаблонам"""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group.html': '/group/leo/',
            'posts/new_post.html': '/new/',
            'new_post.html': '/AA/1/edit/'
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
