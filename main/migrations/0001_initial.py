# Generated by Django 5.2.1 on 2025-06-01 21:31

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('published_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Статья блога',
                'verbose_name_plural': 'Статьи блога',
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image_before', models.ImageField(blank=True, null=True, upload_to='portfolio/before/', verbose_name='Изображение до')),
                ('image_after', models.ImageField(blank=True, null=True, upload_to='portfolio/after/', verbose_name='Изображение после')),
                ('panorama_image', models.ImageField(blank=True, null=True, upload_to='portfolio/panorama/', verbose_name='Панорамное изображение')),
                ('category', models.CharField(max_length=50, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Проект портфолио',
                'verbose_name_plural': 'Проекты портфолио',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('labor_cost_per_m2', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Трудовые затраты за м²')),
                ('base_material_cost_per_m2', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Базовая стоимость материалов за м²')),
                ('category', models.CharField(choices=[('apartment', 'Ремонт квартиры'), ('house', 'Ремонт дома'), ('office', 'Ремонт офиса'), ('warehouse', 'Ремонт склада'), ('facade', 'Фасадные работы'), ('bathroom', 'Ремонт ванной'), ('electrical', 'Электрика'), ('demolition', 'Демонтаж')], max_length=50, verbose_name='Категория')),
                ('image', models.ImageField(blank=True, null=True, upload_to='services/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='Calculation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_type', models.CharField(max_length=100, verbose_name='Тип работы')),
                ('area', models.FloatField(validators=[django.core.validators.MinValueValidator(0.1)], verbose_name='Площадь')),
                ('material', models.CharField(max_length=100, verbose_name='Материал')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Общая стоимость')),
                ('material_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость материалов')),
                ('labor_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость работы')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('in_progress', 'В процессе'), ('completed', 'Завершен')], default='new', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('data', models.JSONField(blank=True, null=True, verbose_name='Дополнительные данные расчёта')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calculations', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Расчёт',
                'verbose_name_plural': 'Расчёты',
            },
        ),
        migrations.CreateModel(
            name='ChatLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('response', models.TextField(blank=True, verbose_name='Ответ')),
                ('language', models.CharField(default='ru', max_length=10, verbose_name='Язык')),
                ('file_path', models.CharField(blank=True, max_length=255, null=True, verbose_name='Путь к файлу')),
                ('audio_path', models.CharField(blank=True, max_length=255, null=True, verbose_name='Путь к аудио')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP-адрес')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Лог чата',
                'verbose_name_plural': 'Логи чата',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя партнёра')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
                ('company', models.CharField(blank=True, max_length=255, verbose_name='Компания')),
                ('partner_type', models.CharField(choices=[('realtor', 'Риелтор/Агентство недвижимости'), ('designer', 'Дизайнер интерьеров'), ('architect', 'Архитектор'), ('business', 'Бизнес-партнёр'), ('other', 'Другое')], max_length=50, verbose_name='Тип партнёрства')),
                ('cities', models.CharField(choices=[('cologne', 'Кёльн'), ('hamburg', 'Гамбург'), ('both', 'Оба города')], max_length=50, verbose_name='Города работы')),
                ('agreement', models.BooleanField(default=False, verbose_name='Согласие с условиями')),
                ('referral_code', models.CharField(max_length=50, unique=True, verbose_name='Реферальный код')),
                ('total_referrals', models.IntegerField(default=0, verbose_name='Количество привлеченных клиентов')),
                ('total_earnings', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Общий заработок')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partners', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Партнёр',
                'verbose_name_plural': 'Партнёры',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, max_length=100, verbose_name='Автор')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Оценка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
    ]
