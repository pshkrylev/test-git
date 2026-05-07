from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Category
from .forms import PostForm

def post_list(request):
    posts = Post.objects.select_related('author', 'category').order_by('-created_at')
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    for cat in categories:
        cat.post_count = Post.objects.filter(category=cat).count()
    return render(request, 'posts/list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(category_id) if category_id else 0,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author', 'category'), pk=pk)
    return render(request, 'posts/detail.html', {'post': post})

@login_required
def post_create(request):
    if not request.user.is_verified:
        return render(request, 'posts/not_verified.html')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/confirm_delete.html', {'post': post})