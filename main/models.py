from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Модель для услуг
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('construction', 'Строительство'),
        ('design', 'Дизайн'),
    ]

    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    image = models.ImageField(upload_to='services/', verbose_name="Изображение")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

# Модель для портфолио
class Portfolio(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_before = models.ImageField(upload_to='portfolio/')
    image_after = models.ImageField(upload_to='portfolio/')
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title

# Модель для расчетов
class Calculation(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calculations')
    work_type = models.CharField(max_length=100)
    area = models.FloatField()
    material = models.CharField(max_length=100)
    include_materials = models.BooleanField(default=False)
    urgency = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    material_cost = models.DecimalField(max_digits=10, decimal_places=2)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.work_type} - {self.total_cost}"

# Модель для отзывов клиентов
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Оценка от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.username}"

# Модель для партнеров
class Partner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partners', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Имя партнера")
    contact_info = models.CharField(max_length=255, verbose_name="Контактная информация")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)  # Новое поле
    email = models.EmailField(verbose_name="Email", blank=True, null=True)  # Новое поле
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
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog/')

    def __str__(self):
        return self.title