from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Group
from .forms import PostForm


def index(request):
    """ view - функция для главной страницы приложения posts."""

    latest = Post.objects.order_by('-pub_date')[:11]
    context = {'posts': latest}
    return render(request, 'index.html', context)


def group_posts(request, slug):
    """ view - функция для страницы сообщества.

    Параметры функции
    ---------
    slug: str
        Слаг группы.
    """

    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all().order_by('-pub_date')[:12]
    context = {'group': group, 'posts': posts}
    return render(request, 'group.html', context)


class NewPostView(LoginRequiredMixin, CreateView):
    """ Класс NewPostView для представления формы создания новой записи.

    Методы класса
    --------
    form_valid(self, form) -- осуществляет проверку заполненой формы.
    Заполняет поле автора поста текущим пользователем.
    """

    # Проверка авторизации
    login_url = reverse_lazy('login')

    template_name = 'new_post.html'
    form_class = PostForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """ Присвоить для поля 'author' значение текущего пользователя и
        вернуть форму."""

        form.instance.author = self.request.user
        return super(NewPostView, self).form_valid(form)
