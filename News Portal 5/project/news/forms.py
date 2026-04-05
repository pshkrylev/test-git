from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Форма для создания/редактирования новостей и статей"""

    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']  # поле type не включаем
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10}),
        }