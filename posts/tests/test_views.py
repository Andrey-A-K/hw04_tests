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
            group=cls.test_group)

    def setUp(self):
        # Создаем клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'about/author.html': reverse('about:author'),
            'about/tech.html': reverse('about:tech'),
            'profile.html':
                reverse('posts:profile',
                        kwargs={'username': self.user.username}),
            'post.html':
                reverse('posts:post', kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id
                }),
            'new_post.html':
                reverse('posts:post_edit', kwargs={
                    'username': self.user.username,
                    'post_id': self.post.id
                }),
            'posts/new_post.html': reverse('posts:new_post'),
            'posts/index.html': reverse('posts:posts_index'),
            'posts/group.html': (
                reverse('posts:group_posts',
                        kwargs={'slug': self.test_group.slug})
            ),
        }
        # Проверяем, что при обращении к name вызывается
        # соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

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

    def test_posts_page_list_is_1(self):
        # Удостоверимся, что на страницу со списком заданий передаётся
        # ожидаемое количество объектов
        response = self.authorized_client.get(reverse('posts:posts_index'))
        self.assertEqual(len(response.context['page']), 1)

    def test_group_page_shows_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': 'leo'}))
        self.assertEqual(response.context['group'].title, 'leo')
        self.assertEqual(
            response.context['group'].description, 'test_description')
        self.assertEqual(response.context['group'].slug, 'leo')

    def test_new_page_shows_correct_context(self):
        """типы полей формы в словаре new соответствуют ожиданиям"""
        response = self.authorized_client.get(reverse('posts:new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

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

    def test_post_edit_page_shows_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'username': self.user.username,
                                       'post_id': self.post.id}))
        self.assertEqual(response.context['user'], self.user)

    def test_post_appeared_on_the_main_page(self):
        """пост появляется на главной странице сайта"""
        response = self.authorized_client.get(reverse('posts:posts_index'))
        self.assertIn(self.post, response.context['post_list'])

    def test_post_appeared_on_the_groups_page(self):
        """пост появляется на странице выбранной группы"""
        response = self.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': 'leo'}))
        self.assertIn(self.post, response.context['posts'])

    def test_post_didnot_appear_on_the_other_groups_page(self):
        """пост не попал в другую группу"""
        response = self.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': 'AA'}))
        self.assertIsNot(self.post, response.context['posts'])
