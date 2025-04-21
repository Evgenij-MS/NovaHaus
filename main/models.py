from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Модель для услуг
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('construction', _('Строительство')),
        ('design', _('Дизайн')),
        ('renovation', _('Ремонт')),
        ('bathroom', _('Ванные комнаты')),
        ('electrical', _('Электрика')),
        ('facade', _('Фасады')),
        ('demolition', _('Демонтаж')),
        ('cleaning', _('Уборка')),
    ]

    title = models.CharField(max_length=100, verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Описание"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"), null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name=_("Категория"))
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name=_("Изображение"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Услуга")
        verbose_name_plural = _("Услуги")

# Модель для портфолио
class Portfolio(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Название"))
    description = models.TextField(verbose_name=_("Описание"))
    image_before = models.ImageField(upload_to='portfolio/before/', blank=True, null=True, verbose_name=_("Изображение до"))
    image_after = models.ImageField(upload_to='portfolio/after/', blank=True, null=True, verbose_name=_("Изображение после"))
    panorama_image = models.ImageField(upload_to='portfolio/panorama/', blank=True, null=True, verbose_name=_("Панорамное изображение"))
    category = models.CharField(max_length=50, verbose_name=_("Категория"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Проект портфолио")
        verbose_name_plural = _("Проекты портфолио")

# Модель для расчетов
class Calculation(models.Model):
    STATUS_CHOICES = [
        ('new', _('Новый')),
        ('in_progress', _('В процессе')),
        ('completed', _('Завершен')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calculations', blank=True, null=True, verbose_name=_("Пользователь"))
    work_type = models.CharField(max_length=100, verbose_name=_("Тип работы"))
    area = models.FloatField(verbose_name=_("Площадь"))
    material = models.CharField(max_length=100, verbose_name=_("Материал"))
    include_materials = models.BooleanField(default=False, verbose_name=_("Включить материалы"))
    urgency = models.CharField(max_length=50, verbose_name=_("Срочность"))
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Общая стоимость"))
    material_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Стоимость материалов"))
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Стоимость работы"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name=_("Статус"))
    start_date = models.DateField(null=True, blank=True, verbose_name=_("Дата начала"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("Дата окончания"))
    data = models.JSONField(blank=True, null=True, verbose_name=_("Дополнительные данные расчёта"))

    def __str__(self):
        return f"{self.work_type} - {self.total_cost}"

    class Meta:
        verbose_name = _("Расчёт")
        verbose_name_plural = _("Расчёты")

# Модель для отзывов клиентов
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True, verbose_name=_("Пользователь"))
    author = models.CharField(max_length=100, blank=True, verbose_name=_("Автор"))
    text = models.TextField(verbose_name=_("Текст отзыва"))
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_("Оценка"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    def __str__(self):
        return f"Отзыв от {self.author or self.user.username if self.user else 'Аноним'}"

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

# Модель для партнеров
class Partner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partners', blank=True, null=True, verbose_name=_("Пользователь"))
    name = models.CharField(max_length=255, verbose_name=_("Имя партнёра"))
    contact_info = models.CharField(max_length=255, blank=True, verbose_name=_("Контактная информация"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Телефон"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("Электронная почта"))
    referral_code = models.CharField(max_length=50, unique=True, verbose_name=_("Реферальный код"))
    total_referrals = models.IntegerField(default=0, verbose_name=_("Количество привлеченных клиентов"))
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Общий заработок"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата регистрации"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата последнего обновления"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Партнёр")
        verbose_name_plural = _("Партнёры")

# Модель для блога
class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Название"))
    content = models.TextField(verbose_name=_("Содержание"))
    published_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата публикации"))
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name=_("Изображение"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Статья блога")
        verbose_name_plural = _("Статьи блога")

# Модель для логов
class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Пользователь"))
    message = models.TextField(verbose_name=_("Сообщение"))
    response = models.TextField(blank=True, verbose_name=_("Ответ"))
    language = models.CharField(max_length=10, default='ru', verbose_name=_("Язык"))
    file_path = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Путь к файлу"))
    audio_path = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Путь к аудио"))
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_("IP-адрес"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    def __str__(self):
        return f"Лог от {self.created_at}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Лог чата")
        verbose_name_plural = _("Логи чата")