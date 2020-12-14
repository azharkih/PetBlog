from django import forms
from django.forms import widgets

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """ Класс PostForm для создания формы связанной с моделью Post."""

    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        widgets = {'image': widgets.ClearableFileInput()}


class CommentForm(forms.ModelForm):
    """ Класс CommentForm для создания формы связанной с моделью Comment."""

    class Meta:
        model = Comment
        fields = ('text',)
