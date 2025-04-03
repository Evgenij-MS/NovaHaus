import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
_ = lambda s: s

# Загрузка переменных окружения
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def get_env_variable(var_name, default=None):
    """Получение переменных окружения с проверкой"""
    value = os.getenv(var_name, default)
    if value is None:
        raise ImproperlyConfigured(f"Переменная окружения {var_name} не установлена.")
    return value

# Основные настройки
SECRET_KEY = get_env_variable('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't', 'y', 'yes')

ALLOWED_HOSTS = [
    'novahaus-koeln.de',
    'www.novahaus-koeln.de',
    'localhost',
    '127.0.0.1',
    'novahaus-eu-5b21cc3bb91d.herokuapp.com',
]

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Сторонние приложения
    'channels',
    'whitenoise.runserver_nostatic',
    'compressor',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'axes',

    # Локальные приложения
    'main',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.middleware.gzip.GZipMiddleware',
]

# Настройки безопасности
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Блокировка ботов и сканеров
DISALLOWED_USER_AGENTS = [
    r'bot', r'scanner', r'curl', r'Chrome/91\.0\.4472\.124',
    r'python-requests', r'Go-http-client', r'Java/',
    r'nikto', r'sqlmap', r'wget', r'libwww-perl',
    r'zgrab', r'okhttp', r'postman'
]

SENSITIVE_URL_PATTERNS = [
    r'^\.env', r'^wp-', r'^config', r'^\.git',
    r'^phpmyadmin', r'^backup', r'\.sql$',
    r'\.bak$', r'\.log$', r'^\.well-known',
    r'^\.ht', r'^\.docker', r'^\.npm'
]

# Настройки django-axes
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # 1 час блокировки
AXES_LOCKOUT_TEMPLATE = 'errors/lockout.html'
AXES_RESET_ON_SUCCESS = True
AXES_DISABLE_ACCESS_LOG = True



# # Оптимизированная конфигурация базы данных
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME', 'novahaus'),
#         'USER': os.getenv('DB_USER', 'postgres'),
#         'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
#         'HOST': os.getenv('DB_HOST', 'localhost'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#         'OPTIONS': {
#             'sslmode': 'disable'  # Явно отключаем SSL для локальной разработки
#         }
#     }
# }



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Для Heroku автоматически переопределяем настройки
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )

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
                'django.template.context_processors.media',
            ],
            'builtins': [
                'django.templatetags.static',
            ],
        },
    },
]

# Статические файлы
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиафайлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Локализация
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    ('de', 'Deutsch'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']

# Двухфакторная аутентификация
OTP_TOTP_ISSUER = 'NovaHaus'

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'axes': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

# Настройки для django-compressor
COMPRESS_ENABLED = not DEBUG
COMPRESS_OFFLINE = not DEBUG
COMPRESS_CSS_FILTERS = [
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# Настройки кеширования
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Настройки для Channels
ASGI_APPLICATION = 'NovaHaus.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.getenv('REDIS_URL', 'redis://localhost:6379/0')],
        },
    },
}

# Настройки CORS для API
CORS_ALLOWED_ORIGINS = [
    "https://novahaus-koeln.de",
    "https://www.novahaus-koeln.de",
]

# Настройки для компрессии
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Кеширование
CACHE_TTL = 60 * 15  # 15 минут

# Sentry для отслеживания ошибок
import sentry_sdk
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


# Настройки для Heroku
if 'DYNO' in os.environ:
    # DEBUG остаётся как было установлено из переменных окружения
    ALLOWED_HOSTS = ['novahaus-koeln.de', 'www.novahaus-koeln.de', 'novahaus-eu.herokuapp.com']
    import django_heroku
    django_heroku.settings(locals(), staticfiles=False)


# Мониторинг
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]


import logging
logger = logging.getLogger(__name__)
logger.info(f"Application started in DEBUG={DEBUG} mode")