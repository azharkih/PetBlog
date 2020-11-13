from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """Класс Post используется для описания модели сообщений пользователей.

    Родительский класс -- models.Model.

    Атрибуты класса
    --------
                                            PK <--
    text : models.TextField()
        текст сообщения
    pub_date : models.DateTimeField()
        дата и время публикации
    author : models.ForeignKey()            FK --> User
        ссылка на модель User
    group : models.ForeignKey()             FK --> Group
        ссылка на модель Group.
    """

    text = models.TextField(verbose_name='Текст сообщения')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата/время публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts', verbose_name='Автор')
    group = models.ForeignKey('Group', on_delete=models.SET_NULL,
                              related_name='posts', null=True, blank=True,
                              verbose_name='Сообщество')

    def __str__(self):
        """Вернуть строковое представление в виде текста поста."""
        return self.text

    class Meta:
        verbose_name_plural = 'Публикации'
        verbose_name = 'Публикация'
        ordering = ['-pub_date']


class Group(models.Model):
    """Класс Group используется для описания модели сообществ.

        Родительский класс -- models.Model.

        Атрибуты класса
        --------
                                                PK <-- Post
        title : models.CharField
            Имя сообщества
        slug : models.SlugField()
            уникальный адрес группы
        description : models.TextField()
            Описание. Текст на странице сообщества.

        Методы класса
        --------
        __str__() -- строковое представление модели.
    """

    title = models.CharField(max_length=200, verbose_name='Имя сообщества')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Сообщества'
        verbose_name = 'Сообщество'
        ordering = ['slug']

    def __str__(self):
        """ Вернуть строковое представление в виде имени сообщества."""

        return self.title
