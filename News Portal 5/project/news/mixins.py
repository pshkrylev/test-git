from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Миксин для проверки, является ли пользователь автором"""

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied("У вас нет прав для доступа к этой странице")


class AuthorOrStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Миксин для проверки, является ли пользователь автором или сотрудником"""

    def test_func(self):
        return (self.request.user.groups.filter(name='authors').exists() or
                self.request.user.is_staff)