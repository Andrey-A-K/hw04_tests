from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
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
        cls.post = Post.objects.create(
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

    def test_new_list_url_exists_at_desired_location(self):
        """Страница /new/ доступна авторизованному пользователю"""
        response = self.authorized_client.get(reverse('posts:new_post'))
        self.assertEqual(response.status_code, 200)

    def test_the_edit_page_is_available_to_the_not_authorized_user(self):
        """Страница редактирования недоступна не автору поста"""
        response = self.authorized_client_2.get(
            reverse('posts:post_edit',
                    kwargs={
                        'username': self.user.username,
                        'post_id': self.post.id
                    }))
        self.assertEqual(response.status_code, 302)

    def test_the_edit_page_is_available_to_the_authorized_user(self):
        """Страница редактирования доступна автору поста"""
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={
                        'username': self.user.username,
                        'post_id': self.post.id
                    }))
        self.assertEqual(response.status_code, 200)

    def test_correct_redirect_of_the_edit_page_without_access_rights(self):
        """правильный редирект страницы редактирования без прав доступа"""
        response = self.guest_client.get(
            reverse('posts:post_edit',
                    kwargs={
                        'username': self.user.username,
                        'post_id': self.post.id
                    }), follow=True)
        self.assertRedirects(response, '/auth/login/?next=/AA/1/edit/')

    def test_urls_uses_correct_template(self):
        """Соответствие страниц шаблонам"""
        templates_url_names = {
            reverse('posts:posts_index'): 'posts/index.html',
            reverse('posts:group_posts',
                    kwargs={'slug': self.test_group.slug}):
                        'posts/group.html',
            reverse('posts:post_edit', kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id
                    }): 'new_post.html',
            reverse('posts:new_post'): 'posts/new_post.html',
            reverse('posts:profile',
                    kwargs={'username': self.user.username}):
                        'profile.html',
            reverse('posts:post',
                    kwargs={'post_id': self.post.id,
                            'username': self.user.username}):
                        'post.html'}
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(template)
                self.assertTemplateUsed(response, reverse_name)

    def test_page_available_everyone(self):
        """Страница  доступна всем"""
        response_code_page = {
            reverse('posts:profile',
                    kwargs={'username': self.user.username}): 200,
            reverse('posts:post',
                    kwargs={'post_id': self.post.id,
                            'username': self.user.username}): 200,
            reverse('posts:group_posts',
                    kwargs={'slug': self.test_group.slug}): 200,
            reverse('posts:posts_index'): 200,
        }
        for template, stat_cod in response_code_page.items():
            with self.subTest():
                response = self.guest_client.get(template)
                self.assertEqual(response.status_code, stat_cod)

    def test_correct_redirect(self):
        """правильный редирект"""
        response_code_page = {
            reverse('posts:post_edit', kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id
                    }): 302,
            reverse('posts:post_edit', kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id
                    }): 302
        }
        for template, stat_cod in response_code_page.items():
            with self.subTest():
                response = self.guest_client.get(template)
                self.assertEqual(response.status_code, stat_cod)
