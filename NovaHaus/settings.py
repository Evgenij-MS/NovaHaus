import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Загрузка переменных окружения
load_dotenv()

# Базовая директория
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')

# Режим отладки
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Разрешенные хосты
ALLOWED_HOSTS = [
    'novahaus-koeln.de',
    'www.novahaus-koeln.de',
    'localhost',
    '127.0.0.1',
]

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'whitenoise.runserver_nostatic',
]

# Промежуточное ПО
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Корневой URL
ROOT_URLCONF = 'NovaHaus.urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI-приложение
WSGI_APPLICATION = 'NovaHaus.wsgi.application'

# База данных
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Локализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиафайлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Ключевое поле по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Кэширование
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

# Настройки для Heroku
if os.getenv('ON_HEROKU'):
    import django_heroku
    django_heroku.settings(locals())