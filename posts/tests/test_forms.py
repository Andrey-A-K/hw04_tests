from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем пользователя
        cls.user = User.objects.create_user(username='AA')
        # Создаем группу
        cls.test_group = Group.objects.create(
            title='leo',
            description='test_description',
            slug='leo')
        # Создадим запись в БД
        cls.post = Post.objects.create(
            text='Тестовый текст',
            pub_date=Post.pub_date,
            author=cls.user,
            group=cls.test_group)

    def setUp(self):
        # Создаем клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        # Подсчитаем количество записей в Post
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый',
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), post_count + 1)
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:posts_index'))
