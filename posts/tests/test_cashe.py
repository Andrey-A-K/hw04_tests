from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.core.cache import cache

from posts.models import Group, Post

User = get_user_model()


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(
            username='AA',
            password='AA'
        )
        cls.group = Group.objects.create(
            title='группа',
            slug='leo'
        )
        cls.post = Post.objects.create(
            text='Тест кеша',
            author=cls.author,
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def test_new_post_creates_new_post(self):
        """Главная страница кэширует отображаемую информацию """
        response = self.guest_client.get(reverse('posts:posts_index'))
        """ Добавляем 2й пост"""
        self.new_post = Post.objects.create(
            text='Тестовая заметка 2',
            author=self.author,
            group=self.group
        )
        """ проверяем, что после добавления новгого поста """
        """ нам отдаются кешированные данные с его отсутствием """
        response_2 = self.guest_client.get(reverse('posts:posts_index'))
        self.assertEqual(response.content, response_2.content)
        """ очищаем кеш """
        cache.clear()
        """ Сравниваем что после добавления"""
        """ поста новые данные не равны старым"""
        response_3 = self.guest_client.get(reverse('posts:posts_index'))
        self.assertNotEqual(response.content, response_3.content)
