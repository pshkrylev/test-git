from django.contrib import admin
from .models import User, Coordinates, Level, Image, Pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fam', 'name', 'phone')
    search_fields = ('email', 'fam', 'name')


@admin.register(Coordinates)
class CoordinatesAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'height')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('winter', 'summer', 'autumn', 'spring')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'user', 'status',
        'moderation_comment_preview', 'moderation_date', 'add_time'
    )
    list_filter = ('status', 'moderation_date', 'add_time')
    search_fields = ('title', 'user__email', 'moderation_comment')
    readonly_fields = ('add_time', 'moderation_date')

    fieldsets = (
        ('Основная информация', {
            'fields': ('beauty_title', 'title', 'other_titles', 'connect')
        }),
        ('Связи', {
            'fields': ('user', 'coords', 'level', 'images')
        }),
        ('Модерация', {
            'fields': ('status', 'moderation_comment', 'moderated_by', 'moderation_date'),
            'classes': ('wide',),
            'description': 'Для отклонения обязательно укажите комментарий'
        }),
        ('Системные поля', {
            'fields': ('add_time',),
            'classes': ('collapse',)
        }),
    )

    def moderation_comment_preview(self, obj):
        """Отображение превью комментария в списке"""
        if obj.moderation_comment:
            return obj.moderation_comment[:50] + ('...' if len(obj.moderation_comment) > 50 else '')
        return '-'

    moderation_comment_preview.short_description = 'Комментарий модератора'

    def save_model(self, request, obj, form, change):
        """При сохранении через админку обновляем дату модерации"""
        if 'status' in form.changed_data:
            obj.moderation_date = timezone.now()
            obj.moderated_by = request.user if request.user.is_authenticated else None
        super().save_model(request, obj, form, change)