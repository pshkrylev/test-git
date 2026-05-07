from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import RegisterForm
from .models import EmailConfirmationToken

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = False
            user.save()
            token = EmailConfirmationToken.objects.create(user=user)
            confirm_url = request.build_absolute_uri(f'/confirm/{token.token}/')
            send_mail(
                subject='Подтверждение регистрации на MMORPG Board',
                message=f'''Здравствуйте, {user.username}!
Для подтверждения регистрации перейдите по ссылке: {confirm_url}
Если вы не регистрировались, проигнорируйте это письмо.''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(request, 'Регистрация успешна! Проверьте почту.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def confirm_email(request, token):
    token_obj = get_object_or_404(EmailConfirmationToken, token=token)
    if token_obj.is_expired():
        messages.error(request, 'Срок действия ссылки истёк.')
        token_obj.delete()
        return redirect('register')
    user = token_obj.user
    user.is_verified = True
    user.save()
    token_obj.delete()
    login(request, user)
    messages.success(request, 'Email подтверждён! Добро пожаловать.')
    return redirect('post_list')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f'Добро пожаловать, {user.username}!')
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})