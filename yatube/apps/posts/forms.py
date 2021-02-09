from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """ Класс PostForm для создания формы связанной с моделью Post."""

    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        widgets = {'text': SummernoteWidget()}


class CommentForm(forms.ModelForm):
    """ Класс CommentForm для создания формы связанной с моделью Comment."""

    class Meta:
        model = Comment
        fields = ('text',)
