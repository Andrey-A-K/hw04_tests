import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем временную папку для медиа-файлов;
        # на момент теста медиа папка будет перопределена
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        # Для тестирования загрузки изображений
        # берём байт-последовательность картинки,
        # состоящей из двух пикселей: белого и чёрного
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        # Создаем пользователя
        cls.user = User.objects.create_user(username='leo')
        # Создаем группу
        cls.test_group = Group.objects.create(
            title='leo',
            description='test_description',
            slug='leo')
        cls.test_group_2 = Group.objects.create(
            title='AA',
            description='test_description_2',
            slug='AA')
        # Создадим запись в БД
        cls.post = Post.objects.create(
            text='Тестовый текст',
            pub_date=Post.pub_date,
            author=cls.user,
            group=cls.test_group,
            image = uploaded)

    def setUp(self):
        # Создаем клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_posts_page_shows_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:posts_index'))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['page'][0]
        author_0 = first_object.author
        test_text_0 = first_object.text
        test_group_0 = first_object.group
        self.assertEqual(author_0, self.user)
        self.assertEqual(test_text_0, 'Тестовый текст')
        self.assertEqual(test_group_0, self.test_group)

    def test_group_page_shows_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': 'leo'}))
        self.assertEqual(response.context['group'].title, 'leo')
        self.assertEqual(
            response.context['group'].description, 'test_description')
        self.assertEqual(response.context['group'].slug, 'leo')

    def test_profile_page_shows_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.context['user'], self.user)

    def test_post_view_page_shows_correct_context(self):
        """Шаблон post_view сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post', kwargs={'username': self.user.username,
                                  'post_id': self.post.id}))
        self.assertEqual(response.context['user'], self.user)
