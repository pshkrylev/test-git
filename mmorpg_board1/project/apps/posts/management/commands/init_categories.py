from django.core.management.base import BaseCommand
from apps.posts.models import Category

class Command(BaseCommand):
    help = 'Инициализирует категории объявлений'

    def handle(self, *args, **options):
        categories = [
            'tanks', 'healers', 'dd', 'traders', 'guild_masters',
            'quest_givers', 'blacksmiths', 'leatherworkers',
            'potion_makers', 'spell_masters'
        ]
        for cat in categories:
            obj, created = Category.objects.get_or_create(name=cat)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана категория: {obj.get_name_display()}'))
            else:
                self.stdout.write(f'Категория уже существует: {obj.get_name_display()}')
        self.stdout.write(self.style.SUCCESS('Категории инициализированы'))