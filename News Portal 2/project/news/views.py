from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class NewsListView(ListView):
    """Страница со списком новостей с пагинацией"""
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 10  # 10 новостей на странице
    ordering = ['-created_at']  # от свежих к старым

    def get_queryset(self):
        return Post.objects.filter(type='news').order_by('-created_at')


class NewsSearchView(ListView):
    """Страница поиска новостей с фильтрацией"""
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(type='news').order_by('-created_at')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetailView(DetailView):
    """Детальная страница новости"""
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_item'

    def get_queryset(self):
        return Post.objects.filter(type='news')


class NewsCreateView(CreateView):
    """Создание новости"""
    model = Post
    form_class = PostForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        # Устанавливаем тип "новость" перед сохранением
        post = form.save(commit=False)
        post.type = 'news'
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    """Редактирование новости"""
    model = Post
    form_class = PostForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type='news')


class NewsDeleteView(DeleteView):
    """Удаление новости"""
    model = Post
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type='news')


class ArticleCreateView(CreateView):
    """Создание статьи"""
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        # Устанавливаем тип "статья" перед сохранением
        post = form.save(commit=False)
        post.type = 'article'
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    """Редактирование статьи"""
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type='article')


class ArticleDeleteView(DeleteView):
    """Удаление статьи"""
    model = Post
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(type='article')