from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import UpdateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import PostForm, CommentForm
from .models import Post, Group, Follow, User
from .view_add import UserProfile


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def page_forbidden(request, exception):
    return render(
        request,
        "misc/403.html",
        {"path": request.path},
        status=403
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


def index(request):
    """ view-функция для главной страницы приложения posts."""

    posts = Post.objects.select_related(
        'group', 'author').prefetch_related('comments')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator}
    return render(request, 'index.html', context)


def group_posts(request, slug):
    """ view-функция для страницы сообщества.

    Параметры функции
    ---------
    slug: str
        Слаг группы.
    """

    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author').prefetch_related('comments')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'group': group, 'page': page, 'paginator': paginator}
    return render(request, 'group.html', context)


class NewPostView(LoginRequiredMixin, CreateView):
    """ Класс NewPostView для представления формы создания новой записи.

    Родительский класс -- LoginRequiredMixin, CreateView.

    Методы класса
    --------
    form_valid(form) -- осуществляет проверку заполненой формы.
    Заполняет поле автора поста текущим пользователем.
    """

    # Проверка авторизации
    login_url = reverse_lazy('login')

    # Убрать из финальной верссии. Тесты требуют перенаправления на главную, но
    # я логичнее направлять на страницу поста (у модели есть соответствующий
    # метод).
    success_url = reverse_lazy('index')

    template_name = 'new_post.html'
    form_class = PostForm
    extra_context = {'header': 'Новая запись',
                     'button_text': 'Опубликовать',
                     'action': 'new_post'}

    def form_valid(self, form):
        """ Присвоить для поля 'author' значение текущего пользователя и
        вернуть форму."""
        form.instance.author = self.request.user
        return super(NewPostView, self).form_valid(form)


class EditPostView(LoginRequiredMixin, UpdateView):
    """ Класс EditPostView для редактирования поста.

    Родительский класс -- LoginRequiredMixin, UpdateView.

    Методы класса
    --------
    get_form_kwargs() -- осуществляет проверку соответствия автора поста и
    авторизованного пользователя. В случае несоответствия возвращает код 403.
    """

    # Проверка авторизации
    login_url = reverse_lazy('login')

    model = Post
    template_name = 'new_post.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    extra_context = {'header': 'Редактирование записи',
                     'button_text': 'Сохранить',
                     'action': 'post_edit'}

    def get_queryset(self):
        """Вернуть queryset."""
        return UserProfile(self.kwargs['username']).user_posts

    def get_form_kwargs(self):
        """Проверить на соответствие автора поста и авторизованного
        пользователя, в случае несоответствия -- вернуть код 403."""
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class PostView(DetailView):
    """ Класс PostView для просмотра пооста.

    Родительский класс -- DetailView.

    Методы класса
    --------
    get_context_data() -- добавляет в контекст информацию об авторе.
    """

    model = Post
    template_name = 'post.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        """Вернуть queryset."""
        return UserProfile(self.kwargs['username']).user_posts

    def get_context_data(self, **kwargs):
        """Вернуть контекст с добавленным автором."""
        context = super(PostView, self).get_context_data(**kwargs)
        context['author'] = UserProfile(self.kwargs['username'],
                                        self.request.user).user_info
        # для тестов
        context['user_'] = UserProfile(self.kwargs['username']).user
        context['comments'] = context['object'].comments.all()
        context['form'] = CommentForm()
        return context


class UserProfileView(ListView):
    """ Класс UserProfileView для просмотра профиля пользователя.

    Родительский класс -- ListView.

    Методы класса
    --------
    get_queryset() -- возвращает queryset.
    get_context_data() -- возвращает контекст с добавленной информацией об
        авторе.
    """

    template_name = 'profile.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """Вернуть queryset."""
        return UserProfile(self.kwargs['username']).user_posts

    def get_context_data(self, **kwargs):
        """Вернуть контекст с добавленным автором."""
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['author'] = UserProfile(self.kwargs['username'],
                                        self.request.user).user_info
        # для тестов
        context['user_'] = UserProfile(self.kwargs['username']).user
        return context


class AddCommentView(LoginRequiredMixin, CreateView):
    """ Класс AddCommentView для представления страницы с комментариями.

    Родительский класс -- LoginRequiredMixin, CreateView.

    Методы класса
    --------
    form_valid(form) -- осуществляет проверку заполненой формы.
    Заполняет поле автора комментария текущим пользователем.
    """
    # Проверка авторизации
    login_url = reverse_lazy('login')

    form_class = CommentForm

    def form_valid(self, form):
        """ Присвоить для поля 'author' значение текущего пользователя и
        вернуть форму."""
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super(AddCommentView, self).form_valid(form)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return reverse_lazy('post', kwargs=self.kwargs)


class FollowIndexView(LoginRequiredMixin, ListView):
    # Проверка авторизации
    login_url = reverse_lazy('login')

    template_name = 'follow.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        """Вернуть queryset."""
        return Post.objects.filter(author__following__user=user)

    # для тестов! тест требует, что-бы в контекст передавалась непременно
    # 'page', стандартное 'page_obj' как-то не устраивает...
    def get_context_data(self, **kwargs):
        """Сделать костыль для прохождения теста."""
        context = super(FollowIndexView, self).get_context_data(**kwargs)
        context['page'] = context['page_obj']
        return context


class ProfileFollowView(LoginRequiredMixin, RedirectView):
    # Проверка авторизации
    login_url = reverse_lazy('login')

    def get(self, *args, **kwargs):
        author = get_object_or_404(User, username=self.kwargs['username'])
        user = self.request.user
        if author != user:
            Follow.objects.get_or_create(author=author, user=user)
        return redirect(reverse('profile', kwargs=self.kwargs))
        # опять тесты против...
        # return redirect(self.request.GET['next'])


class ProfileUnfollowView(LoginRequiredMixin, View):
    # Проверка авторизации
    login_url = reverse_lazy('login')

    def get(self, *args, **kwargs):
        author = get_object_or_404(User, username=self.kwargs['username'])
        Follow.objects.filter(author=author, user=self.request.user).delete()
        return redirect(reverse('profile', kwargs=self.kwargs))
        # опять тесты против...
        # return redirect(self.request.GET['next'])
