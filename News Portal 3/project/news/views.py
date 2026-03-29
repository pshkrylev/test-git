from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from .models import Post
from .forms import PostForm
from .filters import PostFilter
from .mixins import AuthorRequiredMixin


class ProfileView(LoginRequiredMixin, DetailView):
    """Представление профиля пользователя"""
    model = User
    template_name = 'profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Представление редактирования профиля с проверкой аутентификации"""
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)


class BecomeAuthorView(LoginRequiredMixin, UpdateView):
    """Представление для становления автором"""

    def get(self, request, *args, **kwargs):
        authors_group, created = Group.objects.get_or_create(name='authors')
        request.user.groups.add(authors_group)
        return redirect('profile')


class NewsCreateView(AuthorRequiredMixin, CreateView):
    """Создание новости - только для авторов"""
    model = Post
    form_class = PostForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'news'
        return super().form_valid(form)


class NewsUpdateView(AuthorRequiredMixin, UpdateView):
    """Редактирование новости - только для авторов"""
    model = Post
    form_class = PostForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type='news')


class NewsDeleteView(AuthorRequiredMixin, DeleteView):
    """Удаление новости - только для авторов"""
    model = Post
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type='news')


class ArticleCreateView(AuthorRequiredMixin, CreateView):
    """Создание статьи - только для авторов"""
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'article'
        return super().form_valid(form)


class ArticleUpdateView(AuthorRequiredMixin, UpdateView):
    """Редактирование статьи - только для авторов"""
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type='article')


class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    """Удаление статьи - только для авторов"""
    model = Post
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type='article')