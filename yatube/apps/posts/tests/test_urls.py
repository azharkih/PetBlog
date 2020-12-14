from django.core.cache import cache

from .fixtures import TestingStand


class PostsURLTests(TestingStand):
    """ Класс PostsURLTests используется для тестирования urls приложения
    posts.

    Родительский класс -- TestingStand, TestCase.

    Методы класса
    --------
    setUpClass() -- фикстура для проверки urls. Определяются соответствия путей
        и шаблонов для отрисовки страниц, доступные для пользователей с
        различными уровня доступа (Level0 -- для всех, Level2 -- для
        авторизованных, Level2 -- для владельцев)
    test_login_required_url_responsible_for_each() -- проверяет, что страницы со
        свободным доступом доступны всем пользователям.
    test_login_required_url_responsible_for_auth_user() -- проверяет, что
    страницы требующие авторизации доступны авторизованному пользователю и
    страница требующая авторизации автором, доступна для него.
    test_login_author_required_url_not_responsible_for_other_user() --
        проверяет, что страницы требующие авторизации автором, не доступны
        для иных пользователей.
    test_login_required_url_redirect_anonymous_to_login() -- проверяет, что
    страницы требующие авторизации перенаправляют анонимного пользователя на
    страницу логина.
    test_urls_uses_correct_template() -- проверяет, что URL-адрес использует
        соответствующий шаблон.
    test_page_not_found()  -- проверяет, что несуществующая страница возвращает
        код 404.
    """

    @classmethod
    def setUpClass(cls):
        """ Определить соответствия путей и шаблонов для отрисовки страниц.

        Задает атрибуты класса с наборами доступных для пользователей с
        различными уровня доступа страниц и соответствующих им шаблонов
        (Level0 -- для всех, Level2 -- для авторизованных, Level2 -- для
        владельцев)
        """
        super().setUpClass()
        # Страницы со свободным доступом. Level0
        cls.pages_no_login_required = {
            '/': 'index.html',
            # /group/firstgroup/
            '/group/' + PostsURLTests.group1.slug + '/': 'group.html',
            # /test_user_1/
            '/' + PostsURLTests.user1.username + '/': 'profile.html',
            # /test_user_1/1/
            '/' + PostsURLTests.post1.author.username + '/' +
            str(PostsURLTests.post1.id) + '/': 'post.html',
        }
        # Страницы требующие авторизации одним из пользователей. Level1
        cls.pages_login_required = {
            '/new/': 'new_post.html',
            '/follow/': 'follow.html',
        }
        # Страницы требующие авторизации автором. Level2
        cls.pages_login_author_required = {
            # /test_user_1/1/edit
            '/' + PostsURLTests.post1.author.username + '/' +
            str(PostsURLTests.post1.id) + '/edit/': 'new_post.html',
        }

    def test_login_required_url_responsible_for_each(self):
        """Проверить, что страницы со свободным доступом доступны всем
        пользователям."""
        check_list = PostsURLTests.pages_no_login_required
        for reverse_name in check_list.keys():
            with self.subTest(f'url: {reverse_name}'):
                response = self.guest_client.get(reverse_name)
                self.assertEqual(response.status_code, 200)

    def test_login_required_url_responsible_for_auth_user(self):
        """Проверить, что страницы требующие авторизации доступны
        авторизованному пользователю и страница требующая авторизации автором,
        доступна для него."""
        check_list = {**PostsURLTests.pages_login_required,
                      **PostsURLTests.pages_login_author_required
                      }
        for reverse_name in check_list.keys():
            with self.subTest(f'url: {reverse_name}'):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(response.status_code, 200)

    def test_login_author_required_url_not_responsible_for_other_user(self):
        """Проверить, что страницы требующие авторизации автором, не доступны
        для иных пользователей."""
        check_list = PostsURLTests.pages_login_author_required
        for reverse_name in check_list.keys():
            with self.subTest(f'url: {reverse_name}'):
                response = self.authorized_client_alter.get(reverse_name)
                self.assertEqual(response.status_code, 403)

    def test_login_required_url_redirect_anonymous_to_login(self):
        """Проверить, что страницы требующие авторизации перенаправляют
        анонимного пользователя на страницу логина."""
        check_list = {**PostsURLTests.pages_login_required,
                      **PostsURLTests.pages_login_author_required
                      }
        for reverse_name in check_list.keys():
            with self.subTest(f'url: {reverse_name}'):
                response = self.guest_client.get(reverse_name, follow=True)
                self.assertRedirects(response,
                                     '/auth/login/?next=' + reverse_name)

    def test_urls_uses_correct_template(self):
        """Проверить, что URL-адрес использует соответствующий шаблон."""
        check_list = {**PostsURLTests.pages_login_required,
                      **PostsURLTests.pages_login_author_required,
                      **PostsURLTests.pages_no_login_required
                      }
        for reverse_name, template in check_list.items():
            with self.subTest(f'template: {template}, url: {reverse_name}'):
                cache.clear()
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_page_not_found(self):
        """Проверить, что несуществующая страница возвращает код 404."""
        response = self.authorized_client.get('/dshwnnkjx/')
        self.assertEqual(response.status_code, 404)
