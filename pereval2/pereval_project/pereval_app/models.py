from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    """Модель пользователя"""
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    otc = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.fam} {self.name} ({self.email})"


class Coordinates(models.Model):
    """Модель координат"""
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    height = models.IntegerField()

    def __str__(self):
        return f"{self.latitude}, {self.longitude} ({self.height}m)"


class Level(models.Model):
    """Модель уровня сложности"""
    winter = models.CharField(max_length=10, blank=True)
    summer = models.CharField(max_length=10, blank=True)
    autumn = models.CharField(max_length=10, blank=True)
    spring = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"Лето: {self.summer}, Зима: {self.winter}"


class Image(models.Model):
    """Модель изображения"""
    data = models.TextField(verbose_name="Base64 изображение")
    title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title or "Без названия"


class Pass(models.Model):
    """Модель перевала"""

    class Status(models.TextChoices):
        NEW = 'new', 'Новый'
        PENDING = 'pending', 'На модерации'
        ACCEPTED = 'accepted', 'Принят'
        REJECTED = 'rejected', 'Отклонён'

    # Основные поля
    beauty_title = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200)
    other_titles = models.CharField(max_length=200, blank=True)
    connect = models.TextField(blank=True)

    # Временные метки
    add_time = models.DateTimeField(auto_now_add=True)

    # Связи
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passes')
    coords = models.OneToOneField(Coordinates, on_delete=models.CASCADE)
    level = models.OneToOneField(Level, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image, related_name='passes')

    # Статус модерации
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.NEW
    )

    #  НОВОЕ ПОЛЕ: комментарий модератора
    moderation_comment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Комментарий модератора',
        help_text='Причина отклонения или замечания модератора'
    )

    #  НОВОЕ ПОЛЕ: дата последней модерации
    moderation_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата модерации',
        help_text='Дата, когда был изменён статус'
    )

    #  НОВОЕ ПОЛЕ: кто провёл модерацию (опционально)
    moderated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderated_passes',
        verbose_name='Модератор'
    )

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def has_moderation_comment(self):
        """Проверка наличия комментария модератора"""
        return bool(self.moderation_comment)

    class Meta:
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'
        ordering = ['-add_time']