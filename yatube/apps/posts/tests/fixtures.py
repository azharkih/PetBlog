import datetime as dt
import io
import tempfile

from PIL import Image
from django.core.files import File
from django.test import TestCase, Client
from django.test import override_settings

from ..models import Post, Group, Follow, Comment, User


def get_sample_image_file(name):
    file_obj = io.BytesIO()
    image = Image.new("RGBA", size=(50, 50), color=(0, 256, 0))
    image.save(file_obj, 'png')
    file_obj.seek(0)
    return File(file_obj, name=name)


def get_sample_text_file(name):
    file_obj = io.StringIO()
    file_obj.write('test')
    return File(file_obj, name=name)


class TestingStand(TestCase):
    """ Класс TestingStand используется для создания тестового стенда.

    Родительский класс -- TestCase.

    Наследуемые классы -- PostCreateFormTests, GroupModelTest, PostModelTest,
        PostsURLTests, PostsPagesTests.

    Методы класса
    --------
    setUpClass() -- создает фикстуру с тестовой БД и клиентами.
    """

    @classmethod
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUpClass(cls):
        """Задать атрибуты класса для тестирования

        user1, user2 : User
            записи с тестовыми пользователеми.
        group1, group2 : Group
            записи с тестовыми группами.
        post1, post2 : Post
            записи с тестовыми постами.
        guest_client : Client
            неаторизованный клиент
        cls.authorized_client : Client
            клиент авторизованный основным пользователем user1
        cls.authorized_client_alter : Client
            клиент авторизованный пользователем user2
        """
        super().setUpClass()
        # Создаем временную папку для медиа-файлов;
        # на момент теста медиа папка будет перопределена
        # Создаём тестовых пользователей в БД
        cls.user1 = User.objects.create(
            username='test_user_1'
        )
        cls.user2 = User.objects.create(
            username='test_user_2'
        )
        # Создаём тестовое сообщество в БД
        cls.group1 = Group.objects.create(
            title='Первая группа',
            slug='firstgroup',
            description='Красочное описание первой группы'
        )
        cls.group2 = Group.objects.create(
            title='Вторая группа',
            slug='secondgroup',
            description='Скупое описание второй группы'
        )
        # Создаём тестовые сообщения в БД для каждой группы, под разными
        # пользователями
        cls.post1 = Post.objects.create(
            text='Пхах' * 100,
            pub_date=dt.datetime(2020, 10, 10, 10, 10, 10, 101010),
            author=cls.user1,
            group=cls.group1
        )
        image_file = get_sample_image_file('test')
        cls.post2 = Post.objects.create(
            text='Ололол' * 100,
            pub_date=dt.datetime(2020, 11, 11, 11, 11, 11, 111111),
            author=cls.user2,
            group=cls.group2,
            image=File(image_file)
        )
        cls.follow1 = Follow.objects.create(
            user=cls.user1,
            author=cls.user2
        )
        cls.comment1 = Comment.objects.create(
            post=cls.post1,
            author=cls.user1,
            text="Первый комментарий"
        )
        # Создаем неавторизованный клиент
        cls.guest_client = Client()
        # Создаем авторизованных клиентов
        cls.authorized_client = Client()
        cls.authorized_client_alter = Client()
        # Авторизуем пользователей
        cls.authorized_client.force_login(cls.user1)
        cls.authorized_client_alter.force_login(cls.user2)
