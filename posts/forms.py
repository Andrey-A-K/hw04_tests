from .models import Post
from django.forms import ModelForm, Textarea


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ["group", "text"]
        widgets = {
            "text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст'
            }),
        }
        labels = {
            'group': ('Группа'),
            'text': ('Текст'),
        }
