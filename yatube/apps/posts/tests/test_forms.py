import tempfile

from django.test import override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Post
from .fixtures import TestingStand, get_sample_image_file, get_sample_text_file


class PostCreateFormTests(TestingStand):
    """ Класс PostCreateFormTests используется для тестирования forms приложения
    posts.

    Родительский класс -- TestingStand, TestCase.

    Методы класса
    --------
    setUpClass() -- фикстура для проверки forms. Создается форма редактирования
        поста.
    test_create_new_post() -- проверяет, что валидная форма создает запись в
        Posts.
    test_update_post() -- проверяет, что валидная форма изменяет запись в
        Posts.
    test_create_new_comment() -- проверяет, что валидная форма создает запись в
        Comment.
    test_guest_can_not_add_comment() -- проверяет, что неавторизованный клиент
        не может создать комментарий.
    """

    @classmethod
    def setUpClass(cls):
        """ Задать атрибуты класса для тестирования

        form : PostForm
            форма для редактирования с поста.
        """
        super().setUpClass()
        cls.form = PostForm()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_new_post(self):
        """Проверить, что валидная форма создает запись в Posts."""
        posts_count = Post.objects.count()
        image_file = get_sample_image_file('test_form.png')
        form_data = {
            'text': 'Проверка формы на корректность создания поста',
            'image': image_file,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('index'))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, содался ли новый пост с указанными параметрами
        new_post = Post.objects.filter(author=PostCreateFormTests.user1).filter(
            text=form_data['text']).count()
        self.assertEqual(new_post, 1)

    def test_not_create_new_post_with_invalid_file(self):
        """Проверить, что при загрузке не графического файла не создается запись
        в Posts."""
        posts_count = Post.objects.count()
        text_file = get_sample_text_file('test_form.txt')
        form_data = {
            'text': 'Проверка формы на корректность создания поста',
            'image': text_file,
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        # Ответ должен содержать код 200
        self.assertEqual(response.status_code, 200)
        # Проверяем, увеличилось ли число постов не увеличилось
        self.assertEqual(Post.objects.count(), posts_count)

    def test_update_post(self):
        """Проверить, что валидная форма изменяет запись в Posts."""
        old_post = PostCreateFormTests.post1
        form_data = {
            'text': 'Новый текст поста',
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('post_edit',
                    args=[old_post.author.username, str(old_post.id)]
                    ),
            data=form_data,
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response,
                             reverse('post',
                                     args=[old_post.author.username,
                                           str(old_post.id)]))
        # Проверяем, изменился ли текст поста
        update_post = Post.objects.get(id=PostCreateFormTests.post1.id)
        self.assertEqual(update_post.text, form_data['text'])

    def test_create_new_comment(self):
        """Проверить, что валидная форма создает запись в Comment."""
        post = PostCreateFormTests.post1
        form_data = {
            'text': 'Новый комментарий',
        }
        comments_count = post.comments.count()
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('add_comment',
                    args=[post.author.username,
                          str(post.id)]),
            data=form_data,
            follow=True
        )
        # Проверяем, увеличилось ли число комментариев
        self.assertEqual(post.comments.count(), comments_count + 1)

    def test_guest_can_not_add_comment(self):
        """Проверить, что неавторизованный клиент не может создать
        комментарий."""
        post = PostCreateFormTests.post1
        form_data = {
            'text': 'Новый комментарий',
        }
        comments_count = post.comments.count()
        # Отправляем POST-запрос
        response = self.guest_client.post(
            reverse('add_comment',
                    args=[post.author.username,
                          str(post.id)]),
            data=form_data,
            follow=True
        )
        # Проверяем, что число комментариев не увеличилось
        self.assertEqual(post.comments.count(), comments_count)
