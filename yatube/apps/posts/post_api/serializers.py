from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import Comment, Follow, Group, Like, Post, User


class PostSerializer(serializers.ModelSerializer):
    """ Класс PostSerializer описывает сериализатор модели постов.

    Родительский класс -- serializers.ModelSerializer.

    Атрибуты класса
    --------
    author : str
        Юзернейм автора.
    """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """ Класс CommentSerializer описывает сериализатор модели комментариев.

    Родительский класс -- serializers.ModelSerializer.

    Атрибуты класса
    --------
    author : str
        Юзернейм автора.
    """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """ Класс FollowSerializer описывает сериализатор модели подписок.

    Родительский класс -- serializers.ModelSerializer.
    Переопределенные методы -- validate.

    Атрибуты класса
    --------
    user : str
        Юзернейм подписчика.
    following : str
        Юзернейм автора на которого подписываемся.
    """
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault())

    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Такая подписка уже есть'
            )
        ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя')
        return data


class GroupSerializer(serializers.ModelSerializer):
    """ Класс GroupSerializer описывает сериализатор модели сообществ.

    Родительский класс -- serializers.ModelSerializer.
    """

    class Meta:
        fields = ('id', 'title', 'slug')
        model = Group
        read_only_fields = ['slug', ]


class LikeSerializer(serializers.ModelSerializer):
    """ Класс LikeSerializer описывает сериализатор модели лайков.

    Родительский класс -- serializers.ModelSerializer.

    Атрибуты класса
    --------
    author : str
        Юзернейм автора.
    """
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username')

    class Meta:
        fields = ('id', 'user', 'author', 'post')
        model = Like
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'post'],
                message='Этот пост уже лайкнут'
            )
        ]
