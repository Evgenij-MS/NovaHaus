import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
import tempfile
import django_heroku


# Активировать настройки Heroku
django_heroku.settings(locals())


# Загрузка переменных окружения
load_dotenv()

# Базовая директория
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')

# Режим отладки
# DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'  # Используем переменную окружения для DEBUG
DEBUG = True

# Разрешенные хосты
ALLOWED_HOSTS = [
    'novahaus-koeln.de',
    'www.novahaus-koeln.de',
    'localhost',
    '127.0.0.1',
    'novahaus-eu-5b21cc3bb91d.herokuapp.com',
]

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'main',
    'whitenoise.runserver_nostatic',
    'compressor',  # Добавляем django-compressor
    'django_otp',  # Для двухфакторной аутентификации
    'django_otp.plugins.otp_totp',  # Для TOTP (Time-Based One-Time Password)
]

# Промежуточное ПО
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise должен быть сразу после SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middleware.BlockBadBotsMiddleware',  # Middleware для блокировки ботов
    'django.middleware.locale.LocaleMiddleware',
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

# Настройки для статических файлов
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',  # Добавляем CompressorFinder
]

# Медиафайлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Ключевое поле по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Кэширование
# Абсолютный путь к директории кеша
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')

# Создаем директорию, если она не существует
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': CACHE_DIR,  # Используем абсолютный путь
        'TIMEOUT': 300,  # Время жизни кеша в секундах (5 минут)
        'OPTIONS': {
            'MAX_ENTRIES': 1000,  # Максимальное количество записей в кеше
        }
    }
}

# Настройки для django-compressor
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# Настройки для Heroku
if os.getenv('ON_HEROKU'):
    import django_heroku
    django_heroku.settings(locals())

# Настройки безопасности (только для production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # Перенаправление HTTP на HTTPS
    SESSION_COOKIE_SECURE = True  # Безопасные cookies для сессий
    CSRF_COOKIE_SECURE = True  # Безопасные cookies для CSRF
    SECURE_BROWSER_XSS_FILTER = True  # Защита от XSS
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # Включение HSTS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Включение HSTS для поддоменов
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Для прокси

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    ('de', 'Deutsch'),
]

LANGUAGE_CODE = 'ru'

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Добавьте настройки для двухфакторной аутентификации
OTP_TOTP_ISSUER = 'NovaHaus'  # Название компании для TOTP

