from django.db import models
from django.contrib.auth.models import User

# Модель для услуг
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('construction', 'Строительство'),
        ('design', 'Дизайн'),
        ('renovation', 'Ремонт'),
        ('bathroom', 'Ванные комнаты'),
        ('electrical', 'Электрика'),
        ('facade', 'Фасады'),
        ('demolition', 'Демонтаж'),
        ('cleaning', 'Уборка'),
    ]

    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    image = models.ImageField(upload_to='services/', verbose_name="Изображение")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

# Модель для портфолио
class Portfolio(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image_before = models.ImageField(upload_to='portfolio/', verbose_name="Изображение до")
    image_after = models.ImageField(upload_to='portfolio/', verbose_name="Изображение после")
    category = models.CharField(max_length=50, verbose_name="Категория")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Проект портфолио"
        verbose_name_plural = "Проекты портфолио"

# Модель для расчетов
class Calculation(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calculations', verbose_name="Пользователь")
    work_type = models.CharField(max_length=100, verbose_name="Тип работы")
    area = models.FloatField(verbose_name="Площадь")
    material = models.CharField(max_length=100, verbose_name="Материал")
    include_materials = models.BooleanField(default=False, verbose_name="Включить материалы")
    urgency = models.CharField(max_length=50, verbose_name="Срочность")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    material_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость материалов")
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость работы")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    start_date = models.DateField(null=True, blank=True, verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")

    def __str__(self):
        return f"{self.work_type} - {self.total_cost}"

    class Meta:
        verbose_name = "Расчет"
        verbose_name_plural = "Расчеты"

# Модель для отзывов клиентов
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")  # Оценка от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отзыв от {self.user.username}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

# Модель для партнеров
class Partner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partners', null=True, blank=True, verbose_name="Пользователь")
    name = models.CharField(max_length=255, verbose_name="Имя партнера")
    contact_info = models.CharField(max_length=255, verbose_name="Контактная информация")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    referral_code = models.CharField(max_length=50, unique=True, verbose_name="Реферальный код")
    total_referrals = models.IntegerField(default=0, verbose_name="Количество привлеченных клиентов")
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Общий заработок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"

# Модель для блога
class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(verbose_name="Содержание")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    image = models.ImageField(upload_to='blog/', verbose_name="Изображение")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"

# Модель для логов
class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    message = models.TextField(verbose_name="Сообщение")
    language = models.CharField(max_length=10, default='ru', verbose_name="Язык")
    file_path = models.CharField(max_length=255, null=True, blank=True, verbose_name="Путь к файлу")
    audio_path = models.CharField(max_length=255, null=True, blank=True, verbose_name="Путь к аудио")
    ip_address = models.GenericIPAddressField(verbose_name="IP-адрес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Лог от {self.created_at}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Лог чата"
        verbose_name_plural = "Логи чата"