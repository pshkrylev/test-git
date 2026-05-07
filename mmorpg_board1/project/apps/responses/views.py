from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Post
from .models import Response
from .forms import ResponseForm
from notifications.tasks import send_response_notification, send_acceptance_notification

@login_required
def response_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.author == request.user:
        messages.error(request, 'Вы не можете оставить отклик на своё объявление')
        return redirect('post_detail', pk=post.pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.post = post
            response.author = request.user
            response.save()
            send_response_notification.delay(response.id)
            messages.success(request, 'Ваш отклик отправлен')
            return redirect('post_detail', pk=post.pk)
    else:
        form = ResponseForm()
    return render(request, 'responses/form.html', {'form': form, 'post': post})

@login_required
def my_responses(request):
    responses = Response.objects.filter(
        post__author=request.user
    ).select_related('post', 'author').order_by('-created_at')
    post_filter = request.GET.get('post')
    if post_filter:
        responses = responses.filter(post_id=post_filter)
    posts = Post.objects.filter(author=request.user)
    return render(request, 'responses/my_responses.html', {
        'responses': responses,
        'posts': posts,
        'selected_post': int(post_filter) if post_filter else 0,
    })

@login_required
def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk, post__author=request.user)
    response.is_accepted = True
    response.save()
    send_acceptance_notification.delay(response.id)
    messages.success(request, f'Отклик от {response.author.username} принят')
    return redirect('my_responses')

@login_required
def delete_response(request, pk):
    response = get_object_or_404(Response, pk=pk, post__author=request.user)
    response.delete()
    messages.success(request, 'Отклик удалён')
    return redirect('my_responses')