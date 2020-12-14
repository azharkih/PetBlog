from django.shortcuts import get_object_or_404

from .models import User, Follow


class UserProfile:
    """ Класс UserProfile для получения информации о пользователе.

    Атрибуты объекта
    --------
    username : str
        username пользователя
    user: User
        информация о пользователе из БД
    user_info -- информация о пользователе.
    user_posts -- выборка постов пользователя.
    """

    def __init__(self, username, viewer=None):
        self.username = username
        self.viewer = viewer
        self.user = get_object_or_404(User, username=self.username)

    @property
    def user_info(self):
        """ Вернуть словарь с информацией о пользователе."""
        author = self.user
        user_info = {
            'fullname': ' '.join((author.first_name, author.last_name)),
            'username': author.username,
            'quantity_posts': author.posts.count(),
            'quantity_followers': author.following.count(),
            'quantity_following': author.follower.count(),
        }
        if not self.viewer.is_anonymous and self.viewer != author:
            user_info = {**user_info,
                         'is_follow_available': True,
                         'is_following': Follow.objects.filter(
                             author=author, user=self.viewer).exists(),
                         }
        return user_info

    @property
    def user_posts(self):
        """ Вернуть выборку постов пользователя."""
        return self.user.posts.select_related(
            'group').prefetch_related('comments')
