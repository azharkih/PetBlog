from django.db.models import BooleanField, Case, Count, Sum, Value, When
from django.shortcuts import get_object_or_404

from .models import Follow, Post, User


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
            'group').annotate(
            count_comments=Count('comments', distinct=True),
            count_likes=Count('likes', distinct=True),
            is_user_liked=Sum(Case(When(likes__user=self.viewer, then=True),
                                   default=False,
                                   output_field=BooleanField())
                              )
        )


class PostQuerySet:
    """ Класс PostQuerySet для получения выборки данных для запрашивающего
    пользователя.

    Атрибуты объекта
    --------
    username : str
        username пользователя
    user: User
        информация о пользователе из БД
    user_info -- информация о пользователе.
    user_posts -- выборка постов пользователя.
    """

    def __init__(self, user_request):
        self.user_request = user_request

    def get_author_with_stat(self, author):
        """ Вернуть выборку с расшириной информацией о пользователе."""
        author = get_object_or_404(User, username=author)
        user_info = User.objects.annotate(
            count_posts=Count('posts', distinct=True),
            count_followers=Count('following', distinct=True),
            count_following=Count('follower', distinct=True)
        )
        if not self.user_request.is_anonymous and self.user_request != author:
            is_following = Follow.objects.filter(
                author=author, user=self.user_request).exists()
            user_info = user_info.annotate(
                is_follow_available=Value(True, output_field=BooleanField()),
                is_following=Value(is_following, output_field=BooleanField())
            )
        return user_info.get(username=author)

    def get_posts_with_stat(self):
        """ Вернуть выборку постов с расширинной статистикой."""
        posts = Post.objects.select_related('group', 'author').annotate(
            count_comments=Count('comments', distinct=True),
            count_likes=Count('likes', distinct=True))

        if not self.user_request.is_anonymous:
            posts = posts.annotate(
                is_user_liked=Sum(
                    Case(When(likes__user=self.user_request, then=True),
                         default=False,
                         output_field=BooleanField())
                )
            )
        return posts
