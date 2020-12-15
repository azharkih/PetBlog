import re

from django import forms
from django.core.cache import cache
from django.core.paginator import Paginator
from django.urls import reverse

from .fixtures import TestingStand
from ..models import Follow, Post


class PostsPagesTests(TestingStand):
    """ Класс PostsPagesTests используется для тестирования view приложения
    posts.

    Родительский класс -- TestingStand, TestCase.

    Методы класса
    --------
    Вспомогательные
    ---
    subtest_correct_context_in_posts_dict(response, context_object_name) --
        проверяет контекст context_object_name, в полученном ответе response.
    subtest_post_form_fields(response) -- проверяет соответствуют ли поля формы
        создания/редактирования поста, полученной в ответе response, ожидаемым.
    subtest_html_has_img_tag -- проверяет наличие тега <img> в контенте ответа.

    Проверка соответствия шаблонов
    ---
    test_pages_uses_correct_template() -- проверяет, соответствие URL-адресов
        требуемым для построения страницы шаблонам.

    Проверка контекста
    ---
    test_index_page_correct_context() -- проверяет контекст шаблона index.
    test_group_posts_show_correct_context() -- проверяет контекст шаблона
        group_posts.
    test_profile_show_correct_context() -- проверяет контекст шаблона profile.
    test_post_show_correct_context() -- проверяет контекст шаблона post.
    test_create_new_post_correct_context() -- проверяет контекст шаблона
        new_post.
    test_update_post_correct_context() -- проверяет контекст шаблона post_edit.
    test_auth_user_can_follow -- проверяет корректность механизма подписки
        автоизованным пользователем.
    test_auth_user_can_unfollow -- проверяет корректность механизма отписки
        автоизованным пользователем.
    """

    def test_pages_uses_correct_template(self):
        """Проверить, что URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'index.html': reverse('index'),
            'new_post.html': reverse('new_post'),
            'group.html': (reverse('group_posts',
                                   kwargs={'slug': PostsPagesTests.group1.slug})
                           ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                cache.clear()
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def subtest_correct_context_in_posts_dict(self, response,
                                              context_object_name):
        """Проверить контекст context_object_name, в полученном ответе.

        Параметры функции
        ---------
        response: WSGIRequest
            Результат запроса
        context_object_name: str
            Имя объекта в контексте содержащего список постов.
        """
        post_text_0 = response.context.get(context_object_name)[0].text
        post_pub_date_0 = response.context.get(context_object_name)[0].pub_date
        post_author_0 = response.context.get(context_object_name)[0].author
        self.assertEqual(post_text_0, PostsPagesTests.post2.text)
        self.assertEqual(post_pub_date_0, PostsPagesTests.post2.pub_date)
        self.assertEqual(post_author_0, PostsPagesTests.post2.author)

    def subtest_html_has_img_tag(self, response):
        """Проверить наличие тега <img> в контенте ответа."""
        html = response.content.decode()
        img_in_html = re.search(r'<\s*img*\s*\D*\s*src\s*=\s*\"\s*', html)

        self.assertTrue(img_in_html, 'Не отображаются картинки постов')

    def test_index_page_correct_context(self):
        """Проверить контекст шаблона index

        В контекст попадает корректное содержимое и попадают все посты
        (число постов в контексте == 2)."""
        cache.clear()
        response = self.guest_client.get(reverse('index'))
        self.subtest_correct_context_in_posts_dict(response, 'page')
        # имеется ли картинка на странице относящаяся к посту
        self.subtest_html_has_img_tag(response)
        # Записей на странице должно быть 2
        self.assertEqual(len(response.context.get('page')), 2)

    def test_group_posts_show_correct_context(self):
        """Проверить контекст шаблона group_posts

        для постов тестовой группы secondgroup попадает корректное содержимое и
        не попадают посты других групп (число постов в контексте == 1)."""
        response = self.authorized_client.get(
            reverse('group_posts',
                    kwargs={'slug': PostsPagesTests.group2.slug}))
        self.assertEqual(response.context.get('group').title,
                         PostsPagesTests.group2.title)
        self.assertEqual(response.context.get('group').slug,
                         PostsPagesTests.group2.slug)
        self.assertEqual(response.context.get('group').description,
                         PostsPagesTests.group2.description)
        self.subtest_correct_context_in_posts_dict(response, 'page')
        self.subtest_html_has_img_tag(response)
        # Запись для данной группы одна
        self.assertEqual(len(response.context.get('page')), 1)
        # В контекст передается пагинатор
        self.assertIsInstance(response.context.get('paginator'), Paginator)

    def test_profile_show_correct_context(self):
        """Проверить контекст шаблона profile.

        Для тестового пользователя user2 попадает корректное содержимое и не
        попадают посты других пользователей (число постов в контексте == 1)."""
        user = PostsPagesTests.user2
        response = self.authorized_client.get(
            reverse('profile', args=[str(user.username)]))
        self.subtest_correct_context_in_posts_dict(response, 'posts')
        # Запись для данного пользователя одна
        self.assertEqual(len(response.context.get('posts')), 1)
        # В контекст передается пагинатор
        self.assertIsInstance(response.context.get('paginator'), Paginator)
        self.subtest_html_has_img_tag(response)

    def test_post_show_correct_context(self):
        """Проверить контекст шаблона post."""
        test_post = PostsPagesTests.post2
        author = PostsPagesTests.user2
        response = self.authorized_client.get(
            reverse('post', args=[test_post.author.username,
                                  str(test_post.id)]))

        user_info = {
            'first_name': author.first_name,
            'last_name': author.last_name,
            'username': author.username,
            'count_posts': author.posts.count(),
            'count_followers': author.following.count(),
            'count_following': author.follower.count(),
            'is_follow_available': True,
            'is_following': True
        }
        self.assertEqual(response.context.get('author'), user_info)
        self.assertEqual(response.context.get('post'), test_post)
        self.subtest_html_has_img_tag(response)

    def subtest_post_form_fields(self, response):
        """Проверить, что поля формы создания/редактирования поста, полученной
        в ответе, соответствуют ожидаемым.

        Параметры функции
        ---------
        response: WSGIRequest
            Результат запроса."""
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_new_post_correct_context(self):
        """Проверить контекст шаблона new_post."""
        response = self.authorized_client.get(reverse('new_post'))
        self.subtest_post_form_fields(response)

    def test_update_post_correct_context(self):
        """Проверить контекст шаблона post_edit."""
        test_post = PostsPagesTests.post1
        response = self.authorized_client.get(
            reverse('post_edit', args=[test_post.author.username,
                                       str(test_post.id)]))
        self.subtest_post_form_fields(response)

    def test_auth_user_can_follow(self):
        """Проверить может ли авторизованный клиент подписываться."""
        author = PostsPagesTests.user1
        user = PostsPagesTests.user2
        # На всякий случай очищаем возможные подписки
        Follow.objects.filter(author=author).filter(
            user=user).delete()
        # делаем запрос на подписку
        response = self.authorized_client_alter.get(
            reverse('profile_follow', args=[author.username]))
        # Ответ должен содержать код 302
        self.assertEqual(response.status_code, 302)
        # Проверяем, появилась ли подписка
        self.assertTrue(Follow.objects.filter(author=author).filter(
            user=user).exists())

    def test_auth_user_can_unfollow(self):
        """Проверить может ли авторизованный клиент отписываться."""
        author = PostsPagesTests.user1
        user = PostsPagesTests.user2
        # Подписываем автора, если это не сделано ранее
        Follow.objects.get_or_create(author=author, user=user)
        # Проверяем, появилась ли подписка
        self.assertTrue(Follow.objects.filter(author=author).filter(
            user=user).exists())
        # делаем запрос на отписку
        response = self.authorized_client_alter.get(
            reverse('profile_unfollow', args=[author.username]))
        # Ответ должен содержать код 302
        self.assertEqual(response.status_code, 302)
        # Проверяем, удалилась ли подписка
        self.assertFalse(Follow.objects.filter(author=author).filter(
            user=user).exists())

    def test_cashing_index_page(self):
        """Проверить работу кэширования index"""
        cache.clear()
        response = self.authorized_client.get(reverse('index'))
        count_posts = Post.objects.count()
        self.assertEqual(len(response.context['page']), count_posts,
                         'В контекст передаются не все записи')
        Post.objects.create(text='тест', author=PostsPagesTests.user2)
        self.assertEqual(count_posts + 1, Post.objects.count(),
                         'При проверке кэширования не удалось создать пост')
        response2 = self.authorized_client.get(reverse('index'))
        # Контент на странице должен остаться неизменным
        self.assertEqual(len(response.content.decode()),
                         len(response2.content.decode()),
                         'Кэширование главной страницы не работает')
        # Очистим, запросим и посчитаем
        cache.clear()
        response3 = self.authorized_client.get(reverse('index'))
        # Контент на странице должен обновиться
        self.assertNotEqual(len(response.content.decode()),
                            len(response3.content.decode()),
                            'Очистка кэша главной страницы не работает')
