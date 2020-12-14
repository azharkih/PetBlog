from django.test import TestCase

from .fixtures import TestingStand


class GroupModelTest(TestingStand):
    """ Класс GroupModelTest используется для тестирования модели Group
    приложения posts.

    Родительский класс -- TestingStand, TestCase.

    Методы класса
    --------
    test_verbose_name() -- проверяет, что verbose_name в полях совпадает с
        ожидаемым.
    test_help_text() -- проверяет, что help_text в полях совпадает с ожидаемым.
    test_object_name_equal_title() -- проверяет, что __str__  group возвращает
    значение == названию сообщества.
    """

    def test_verbose_name(self):
        """Проверить, что verbose_name в полях совпадает с ожидаемым."""
        group = GroupModelTest.group1
        field_verboses = {
            'title': 'Имя сообщества',
            'slug': 'Слаг',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """Проверить, что help_text в полях совпадает с ожидаемым."""
        group = GroupModelTest.group1
        field_help_texts = {
            'title': 'Назовите сообщество',
            'slug': 'Укажите псевдоним сообщества',
            'description': 'Опишите свое сообщество',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)

    def test_object_name_equal_title(self):
        """Проверить, что __str__  group возвращает значение == названию
        сообщества."""
        group = GroupModelTest.group1
        expected_object_name = group.title
        self.assertEquals(expected_object_name, str(group))


class PostModelTest(TestingStand, TestCase):
    """ Класс GroupModelTest используется для тестирования модели Post
    приложения posts.

    Родительский класс -- TestingStand, TestCase.

    Методы класса
    --------
    test_verbose_name() -- проверяет, что verbose_name в полях совпадает с
        ожидаемым.
    test_help_text() -- проверяет, что help_text в полях совпадает с ожидаемым.
    test_object_name_is_15_symbols_of_title() -- проверяет, что __str__  post
        возвращает значение == 15 первым символам сообщения.
    """

    def test_verbose_name(self):
        """Проверить, что verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post1
        field_verboses = {
            'text': 'Текст сообщения',
            'pub_date': 'Дата/время публикации',
            'author': 'Автор',
            'group': 'Сообщество',
            'image': 'Изображение',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """Проверить, что help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post1
        field_help_texts = {
            'text': 'Введите текст сообщения',
            'pub_date': 'Укажите дату и время публикации',
            'author': 'Укажите автора сообщения',
            'group': 'Укажите сообщество в котором публикуется запись',
            'image': 'Выберите изображение к сообщению',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)

    def test_object_name_is_15_symbols_of_title(self):
        """Проверить, что __str__  post возвращает значение == 15 первым
        символам сообщения."""
        post = PostModelTest.post1
        expected_object_name = post.text[:15] + "..."
        self.assertEquals(expected_object_name, str(post))


class CommentModelTest(TestingStand, TestCase):
    """ Класс CommentModelTest используется для тестирования модели Comment
    приложения posts.

    Родительский класс -- TestingStand, TestCase.

    Методы класса
    --------
    test_verbose_name() -- проверяет, что verbose_name в полях совпадает с
        ожидаемым.
    test_help_text() -- проверяет, что help_text в полях совпадает с ожидаемым.
    test_object_name_is_15_symbols_of_title() -- проверяет, что __str__  post
        возвращает значение == 15 первым символам комментария.
    """

    def test_verbose_name(self):
        """Проверить, что verbose_name в полях совпадает с ожидаемым."""
        comment = CommentModelTest.comment1
        field_verboses = {
            'post': 'Сообщение',
            'author': 'Автор',
            'text': 'Текст комментария',
            'created': 'Дата/время комментария',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    comment._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """Проверить, что help_text в полях совпадает с ожидаемым."""
        comment = CommentModelTest.comment1
        field_help_texts = {
            'post': 'Укажите комментируемое сообщение',
            'author': 'Укажите автора комментария',
            'text': 'Введите текст комментария',
            'created': 'Укажите дату и время комментария',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    comment._meta.get_field(value).help_text, expected)

    def test_object_name_is_15_symbols_of_title(self):
        """Проверить, что __str__  post возвращает значение == 15 первым
        символам сообщения."""
        comment = CommentModelTest.comment1
        expected_object_name = comment.text[:15] + "..."
        self.assertEquals(expected_object_name, str(comment))


class FollowModelTest(TestingStand, TestCase):
    """ Класс FollowModelTest используется для тестирования модели Follow
    приложения posts.

    Родительский класс -- TestingStand, TestCase.

    Методы класса
    --------
    test_verbose_name() -- проверяет, что verbose_name в полях совпадает с
        ожидаемым.
    test_help_text() -- проверяет, что help_text в полях совпадает с ожидаемым.
    test_object_name_equal_title() -- проверяет, что __str__  group возвращает
    значение отражающее кто на кого подписан.
    """

    def test_verbose_name(self):
        """Проверить, что verbose_name в полях совпадает с ожидаемым."""
        follow = FollowModelTest.follow1
        field_verboses = {
            'user': 'Подписчик',
            'author': 'Автор',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    follow._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """Проверить, что help_text в полях совпадает с ожидаемым."""
        follow = FollowModelTest.follow1
        field_help_texts = {
            'user': 'Укажите подписчика',
            'author': 'Укажите на какого автора подписываемся',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    follow._meta.get_field(value).help_text, expected)

    def test_object_name_equal_title(self):
        """Проверить, что __str__  group возвращает значение отражающее кто на
        кого подписан."""
        follow = FollowModelTest.follow1
        expected_object_name = f'{follow.user} подписан на {follow.author}'
        self.assertEquals(expected_object_name, str(follow))
