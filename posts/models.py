from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('текст поста',
                            help_text='Напишите, о чем ваш пост')
    pub_date = models.DateTimeField("date published",
                                    auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="posts")
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              verbose_name="группа",
                              related_name="group_posts",
                              help_text='Выберите группу из списка')

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:15]
