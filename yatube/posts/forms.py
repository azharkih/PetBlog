from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """ Класс PostForm для создания формы связанной с моделью Post."""

    class Meta:
        model = Post
        fields = ('text', 'group')
        help_texts = {'text': 'Введите текст сообщения',
                      'group': 'Укажите сообщество'}
