from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import PostForm, CommentForm
from .models import Post, Group, Follow, User, Like
from .view_add import UserProfile, PostQuerySet


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


class MainIndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 10
    extra_context = {'type_index': 'main',
                     'title': 'Последние обновления на сайте'}

    def get_queryset(self):
        """Вернуть queryset."""
        queryset = PostQuerySet(self.request.user)
        return queryset.get_posts_with_stat()


class FollowIndexView(LoginRequiredMixin, MainIndexView):
    login_url = reverse_lazy('login')
    extra_context = {'type_index': 'follow',
                     'title': 'Сообщения избранных авторов'}

    def get_queryset(self):
        return super(FollowIndexView, self).get_queryset().filter(
            author__following__user=self.request.user)


class LikeIndexView(LoginRequiredMixin, MainIndexView):
    login_url = reverse_lazy('login')
    extra_context = {'type_index': 'like',
                     'title': 'Понравившееся'}

    def get_queryset(self):
        return super(LikeIndexView, self).get_queryset().filter(
            is_user_liked=True)


class GroupPostsView(MainIndexView):
    template_name = 'group.html'

    def get_queryset(self):
        return super(GroupPostsView, self).get_queryset().filter(
            group__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        context = super(GroupPostsView, self).get_context_data(**kwargs)
        context['group'] = group
        return context


class UserProfileView(MainIndexView):
    """ Класс UserProfileView для просмотра профиля пользователя.

    Родительский класс -- MainIndexView.

    Методы класса
    --------
    get_queryset() -- возвращает queryset.
    get_context_data() -- возвращает контекст с добавленной информацией об
        авторе.
    """

    template_name = 'profile.html'

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        queryset = PostQuerySet(self.request.user)
        return queryset.get_posts_with_stat().filter(
            author=author)

    def get_context_data(self, **kwargs):
        """Вернуть контекст с добавленным автором."""
        context = super(UserProfileView, self).get_context_data(**kwargs)
        queryset = PostQuerySet(self.request.user)
        context['author'] = queryset.get_author_with_stat(
            self.kwargs['username'])
        return context


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
        author = get_object_or_404(User, username=self.kwargs['username'])
        queryset = PostQuerySet(self.request.user)
        return queryset.get_posts_with_stat().filter(
            author=author)

    def get_context_data(self, **kwargs):
        """Вернуть контекст с добавленным автором."""
        context = super(PostView, self).get_context_data(**kwargs)
        queryset = PostQuerySet(self.request.user)
        context['author'] = queryset.get_author_with_stat(
            self.kwargs['username'])
        context['form'] = CommentForm()
        context['comments'] = context['object'].comments.all()

        return context


class NewPostView(LoginRequiredMixin, CreateView):
    """ Класс NewPostView для представления формы создания новой записи.

    Родительский класс -- LoginRequiredMixin, CreateView.

    Методы класса
    --------
    form_valid(form) -- осуществляет проверку заполненой формы.
    Заполняет поле автора поста текущим пользователем.
    """
    login_url = reverse_lazy('login')
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


class ProfileFollowView(LoginRequiredMixin, View):
    # Проверка авторизации
    login_url = reverse_lazy('login')

    def get(self, *args, **kwargs):
        author = get_object_or_404(User, username=self.kwargs['username'])
        user = self.request.user
        if author != user:
            Follow.objects.get_or_create(author=author, user=user)
        return redirect(
            self.request.GET.get('next',
                                 reverse('profile', kwargs=self.kwargs)
                                 )
        )


class ProfileUnfollowView(LoginRequiredMixin, View):
    # Проверка авторизации
    login_url = reverse_lazy('login')

    def get(self, *args, **kwargs):
        author = get_object_or_404(User, username=self.kwargs['username'])
        Follow.objects.filter(author=author, user=self.request.user).delete()
        return redirect(
            self.request.GET.get('next',
                                 reverse('profile', kwargs=self.kwargs)
                                 )
        )


class PostLikeView(LoginRequiredMixin, View):
    # Проверка авторизации
    login_url = reverse_lazy('login')

    def get(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        Like.objects.get_or_create(post=post, user=self.request.user)
        back_reference = f"{self.request.GET['next']}" \
                         f"#post_{self.kwargs['post_id']}"
        return redirect(back_reference)


class PostUnlikeView(LoginRequiredMixin, View):
    # Проверка авторизации
    login_url = reverse_lazy('login')

    def get(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        Like.objects.filter(post=post, user=self.request.user).delete()
        back_reference = f"{self.request.GET['next']}" \
                         f"#post_{self.kwargs['post_id']}"
        return redirect(back_reference)
