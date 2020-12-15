from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse

from sorl.thumbnail import delete as delete_tumbnails
from sorl.thumbnail import get_thumbnail

User = get_user_model()


def author_directory_path(instance, filename):
    """Вернуть путь к каталогу с изображениями автора.

    файл будет загружен в MEDIA_ROOT/user_<id>/<filename>"""
    return 'posts/{0}/{1}'.format(instance.author.username, filename)


class Post(models.Model):
    """Класс Post используется для описания модели сообщений пользователей.

    Родительский класс -- models.Model.

    Атрибуты класса
    --------
                                            PK <-- Comment, Like
    text : models.TextField()
        текст сообщения
    pub_date : models.DateTimeField()
        дата и время публикации
    author : models.ForeignKey()            FK --> User
        ссылка на модель User
    group : models.ForeignKey()             FK --> Group
        ссылка на модель Group.
    image : models.ImageField()
        изображение в сообщении.

    Методы класса
    --------
    __str__() -- строковое представление модели.
    get_absolute_url() -- возвращает путь для просмотра страницы с созданной
        записью.
    clear_thumbnails() --
    get_post_image() --
    delete() --
    """

    text = models.TextField(
        verbose_name='Текст сообщения',
        help_text='Введите текст сообщения'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата/время публикации',
        auto_now_add=True,
        help_text='Укажите дату и время публикации'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='Укажите автора сообщения'
    )
    group = models.ForeignKey(
        'Group',
        verbose_name='Сообщество',
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
        help_text='Укажите сообщество в котором публикуется запись'
    )
    image = models.ImageField(
        'Изображение',
        # upload_to=author_directory_path,
        # Для тестов
        upload_to='posts/',
        blank=True,
        null=True,
        help_text='Выберите изображение к сообщению'
    )

    class Meta:
        verbose_name_plural = 'Публикации'
        verbose_name = 'Публикация'
        ordering = ['-pub_date']

    def __str__(self):
        """Вернуть строковое представление в виде текста поста. Если
        сообщение превышает 15 символов вернуть первые 15 символов и '...'"""
        if len(self.text) > 15:
            return self.text[:15] + "..."
        return self.text

    def get_absolute_url(self):
        """Вернуть путь страницы для просмотра созданной записи."""
        return reverse('post', args=[str(self.author.username), str(self.id)])

    def clear_thumbnails(self):
        """Очистить ссылки на кэшированные изображения."""
        delete_tumbnails(self.image)

    def get_post_image(self):
        """Получить изображение для отображения в посте."""
        return get_thumbnail(self.image, '960x339', crop='center', quality=95)

    def delete(self):
        """При удалении записи удалить все ссылаемые объекты."""
        obj = Post.objects.get(pk=self.pk)
        obj.clear_thumbnails()
        super(Post, self).delete()


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

    title = models.CharField(
        verbose_name='Имя сообщества',
        max_length=200,
        help_text='Назовите сообщество'
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text='Укажите псевдоним сообщества'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Опишите свое сообщество'
    )

    class Meta:
        verbose_name_plural = 'Сообщества'
        verbose_name = 'Сообщество'
        ordering = ['slug']

    def __str__(self):
        """ Вернуть строковое представление в виде имени сообщества."""
        return self.title


class Comment(models.Model):
    """Класс Comment используется для описания модели комментариев к сообщениям
     пользователей.

    Родительский класс -- models.Model.

    Атрибуты класса
    --------
                                            PK <--
    post : models.ForeignKey()              FK --> Post
        ссылка на модель Post.
    author : models.ForeignKey()            FK --> User
        ссылка на модель User
    text : models.TextField()
        текст сообщения
    created : models.DateTimeField()
        дата и время публикации

    Методы класса
    --------
    __str__() -- строковое представление модели.
    """

    post = models.ForeignKey(
        'Post',
        verbose_name='Сообщение',
        on_delete=models.CASCADE,
        related_name='comments',
        null=False,
        blank=False,
        help_text='Укажите комментируемое сообщение'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Укажите автора комментария'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    created = models.DateTimeField(
        verbose_name='Дата/время комментария',
        auto_now_add=True,
        help_text='Укажите дату и время комментария'
    )

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['-created']

    def __str__(self):
        """Вернуть строковое представление в виде текста комментария. Если
        сообщение превышает 15 символов вернуть первые 15 символов и '...'"""
        if len(self.text) > 15:
            return self.text[:15] + "..."
        return self.text


class Follow(models.Model):
    """ Класс Follow используется для описания модели подписок.

    Родительский класс -- models.Model.

    Атрибуты класса
    --------
                                            PK <--
    user : models.ForeignKey()              FK --> User
        ссылка на модель User
    author : models.ForeignKey()            FK --> User
        ссылка на модель User

        Методы класса
        --------
        __str__() -- строковое представление модели.
    """

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
        help_text='Укажите подписчика'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
        help_text='Укажите на какого автора подписываемся'
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'
        constraints = [UniqueConstraint(fields=['user', 'author'],
                                        name='unique_following')]

    def __str__(self):
        """ Вернуть строковое представление."""
        return f'{self.user} подписан на {self.author}'


class Like(models.Model):
    """ Класс Like используется для описания модели лаков к постам.

    Родительский класс -- models.Model.

    Атрибуты класса
    --------
                                            PK <--
    user : models.ForeignKey()              FK --> User
        ссылка на модель User
    post : models.ForeignKey()              FK --> Post
        ссылка на модель Post

        Методы класса
        --------
        __str__() -- строковое представление модели.
    """

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='likes',
        help_text='Укажите пользователя'
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Сообщение',
        on_delete=models.CASCADE,
        related_name='likes',
        help_text='Укажите к какому посту лайк'
    )

    class Meta:
        verbose_name_plural = 'Лайки'
        verbose_name = 'Лайк'
        constraints = [UniqueConstraint(fields=['user', 'post'],
                                        name='unique_like')]

    def __str__(self):
        """ Вернуть строковое представление."""
        return f'{self.user} оценил пост {self.post_id}'
