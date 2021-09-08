from .models import Post, Comment
from django import forms
from django.forms import Textarea


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст'
            }),
        }
        labels = {
            'group': ('Группа'),
            'text': ('Текст'),
            'image': ('Изображение'),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст'
            }),
        }

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ["text"]
#         widgets = {"text": forms.Textarea(attrs={"cols": 80, "row": 5}), }
