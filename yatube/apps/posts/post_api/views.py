from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          LikeSerializer, PostSerializer)
from ..models import Comment, Follow, Group, Like, Post


class CreateAndListViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """ Класс PostViewSet используется для обеспечения `create()` и `list()`.
    """
    pass


class PostViewSet(viewsets.ModelViewSet):
    """ Класс PostViewSet используется для обработки api-запросов на операции
    CRUD модели Post.

    Родительский класс -- viewsets.ModelViewSet.
    Переопределенные атрибуты -- queryset, serializer_class, permission_classes.
    Переопределенные методы -- perform_create.
    """
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ Класс CommentViewSet используется для обработки api-запросов на операции
    CRUD модели Comment.

    Родительский класс -- viewsets.ModelViewSet.
    Переопределенные атрибуты -- queryset, serializer_class, permission_classes.
    Переопределенные методы -- perform_create, get_queryset.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self, post_id=None):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post=post)


class GroupViewSet(CreateAndListViewSet):
    """
    Класс GroupViewSet используется для обработки api-запросов на операции
    CRUD модели Group.

    Родительский класс -- viewsets.ModelViewSet.
    Переопределенные атрибуты -- queryset, serializer_class, permission_classes.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]


class LikeViewSet(viewsets.ModelViewSet):
    """
    Класс LikeViewSet используется для обработки api-запросов на операции
    CRUD модели Like.

    Родительский класс -- viewsets.ModelViewSet.
    Переопределенные атрибуты -- serializer_class, permission_classes.
    Переопределенные методы -- perform_create, get_queryset.
    """
    serializer_class = LikeSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self, post_id=None):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        return Like.objects.filter(post=post)


class FollowViewSet(CreateAndListViewSet):
    """
    Класс FollowViewSet используется для обработки api-запросов на операции
    CRUD модели Follow.

    Родительский класс -- viewsets.ModelViewSet.
    Переопределенные атрибуты -- queryset, serializer_class, permission_classes.
    Переопределенные методы -- get_queryset.
    """
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)
