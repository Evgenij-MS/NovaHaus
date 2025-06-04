import re
import os
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

# Загрузка .env в самом начале
load_dotenv()

# Надежная настройка DEBUG с приоритетом для runserver
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 't', 'y', 'yes')
if 'runserver' in sys.argv and not any(arg.startswith('--debug') for arg in sys.argv):
    DEBUG = True
    os.environ['DJANGO_DEBUG'] = 'True'

# Логгер с UTF-8 фильтром для Windows
class UTF8EncodingFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = record.msg.encode('utf-8', errors='replace').decode('utf-8')
        return True

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

def get_env_variable(var_name, default=None):
    """Получение переменной окружения с логированием."""
    value = os.getenv(var_name, default)
    if value is None:
        logger.warning(f"Переменная окружения {var_name} отсутствует. Используем значение по умолчанию: {default}")
    return value

# SECRET_KEY должен быть задан
SECRET_KEY = get_env_variable('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY не установлен в переменных окружения")

# Фильтрация ALLOWED_HOSTS
allowed_hosts_str = get_env_variable('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]
ALLOWED_HOSTS.extend([
    'novahaus-eu.herokuapp.com',
    'novahaus-eu-5b21cc3bb91d.herokuapp.com',
    'novahaus-koeln.de',
    'www.novahaus-koeln.de',
    'novahaus-hamburg.de',
    'www.novahaus-hamburg.de'
])

# ========== Безопасность ==========
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# ==================================

ROOT_URLCONF = 'NovaHaus.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'channels',
    'whitenoise.runserver_nostatic',
    'compressor',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'axes',
    'django_extensions',
    'main',
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'main.middleware.BlockBadBotsMiddleware',
]

# Логирование с обработкой кодировки
LOG_DIR = BASE_DIR / 'logs'
if not LOG_DIR.exists():
    LOG_DIR.mkdir()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'utf8_encoding': {'()': UTF8EncodingFilter},
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'django.log',
            'formatter': 'verbose',
            'filters': ['utf8_encoding'],
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['utf8_encoding'],
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'main': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
    },
}

# Sentry только для production
if not DEBUG:
    sentry_dsn = os.getenv('SENTRY_DSN')
    if sentry_dsn and sentry_dsn.startswith('https://'):
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration

        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[
                DjangoIntegration(),
                LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
            ],
            traces_sample_rate=1.0,
            send_default_pii=True,
            environment='production'
        )
        logger.info("Sentry инициализирован для production")

        # Добавляем Sentry handler
        LOGGING['handlers']['sentry'] = {
            'level': 'ERROR',
            'class': 'sentry_sdk.integrations.logging.SentryHandler',
            'formatter': 'verbose',
        }
        for logger_name in LOGGING['loggers']:
            LOGGING['loggers'][logger_name]['handlers'].append('sentry')
    else:
        logger.warning("Sentry не инициализирован: SENTRY_DSN отсутствует или некорректен")

# ========== Кэш и Redis ==========
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
    CHANNEL_LAYERS = {'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}
else:
    redis_url = os.getenv('REDISCLOUD_URL', 'redis://localhost:6379/0')
    ssl_params = {'ssl_cert_reqs': None} if 'rediss://' in redis_url else {}

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': redis_url,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': ssl_params,
            }
        }
    }
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [(redis_url, ssl_params)],
            },
        },
    }

CACHE_TTL = 60 * 15
# =================================

# Локализация
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Europe/Berlin'

LANGUAGE_CODE = 'de'
LANGUAGES = [
    ('de', 'Deutsch'),
    ('en', 'English'),
    ('tr', 'Türkçe'),
    ('ru', 'Русский'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 31536000  # 1 год

# Безопасность: блокировка ботов
ALLOWED_CRAWLERS = [
    re.compile(r'googlebot', re.IGNORECASE),
    re.compile(r'bingbot', re.IGNORECASE),
    re.compile(r'yandexbot', re.IGNORECASE),
]

DISALLOWED_USER_AGENTS = [
    re.compile(r'bot', re.IGNORECASE),
    re.compile(r'scanner', re.IGNORECASE),
    re.compile(r'Java/', re.IGNORECASE),
    re.compile(r'nikto', re.IGNORECASE),
    re.compile(r'sqlmap', re.IGNORECASE),
    re.compile(r'wget', re.IGNORECASE),
    re.compile(r'libwww-perl', re.IGNORECASE),
    re.compile(r'zgrab', re.IGNORECASE),
    re.compile(r'okhttp', re.IGNORECASE),
    re.compile(r'postman', re.IGNORECASE)
]

if not os.getenv("ALLOW_CURL", "False") == "True":
    DISALLOWED_USER_AGENTS.extend([
        re.compile(r'curl', re.IGNORECASE),
        re.compile(r'python-requests', re.IGNORECASE),
        re.compile(r'Go-http-client', re.IGNORECASE),
    ])

SENSITIVE_URL_PATTERNS = [
    re.compile(r'(^|/)\.env$', re.IGNORECASE),
    re.compile(r'(^|/)wp-', re.IGNORECASE),
    re.compile(r'(^|/)config', re.IGNORECASE),
    re.compile(r'(^|/)backup', re.IGNORECASE),
    re.compile(r'(^|/)\.git', re.IGNORECASE),
    re.compile(r'\.sql$', re.IGNORECASE),
    re.compile(r'\.bak$', re.IGNORECASE),
    re.compile(r'\.log$', re.IGNORECASE),
    re.compile(r'(^|/)phpmyadmin', re.IGNORECASE),
]

# Защита от брутфорса
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_LOCKOUT_TEMPLATE = 'errors/lockout.html'
AXES_RESET_ON_SUCCESS = True
AXES_DISABLE_ACCESS_LOG = True

# ========== БАЗА ДАННЫХ ==========
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'postgres://postgres:Okro.123@localhost:5432/NH'),
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}
# =================================

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
                'django.template.context_processors.static',
            ],
            'builtins': [
                'django.templatetags.static',
                'django.templatetags.i18n',
            ],
        },
    },
]

# Статические файлы
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Дополнительные настройки
OTP_TOTP_ISSUER = 'NovaHaus'

# Compressor
COMPRESS_ENABLED = not DEBUG
COMPRESS_OFFLINE = not DEBUG
COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']

# ASGI
ASGI_APPLICATION = 'NovaHaus.asgi.application'

# CORS/CSRF
CORS_ALLOWED_ORIGINS = [
    "https://novahaus-koeln.de",
    "https://www.novahaus-koeln.de",
    "https://novahaus-hamburg.de",
    "https://www.novahaus-hamburg.de",
]

CSRF_TRUSTED_ORIGINS = [
    'https://novahaus-koeln.de',
    'https://www.novahaus-koeln.de',
    'https://novahaus-eu.herokuapp.com',
    'https://novahaus-hamburg.de',
    'https://www.novahaus-hamburg.de',
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# PWA
PWA_APP_NAME = 'NovaHaus'
PWA_APP_DESCRIPTION = "Renovation services in Cologne and Hamburg"
PWA_APP_THEME_COLOR = '#005B99'
PWA_APP_BACKGROUND_COLOR = '#FFFFFF'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {'src': '/static/images/logo.png', 'sizes': '192x192', 'type': 'image/png'},
    {'src': '/static/images/logo.png', 'sizes': '512x512', 'type': 'image/png'},

    {'src': '/static/images/favicon/android-chrome-192x192.png', 'sizes': '192x192', 'type': 'image/png'},
    {'src': '/static/images/favicon/android-chrome-512x512.png', 'sizes': '512x512', 'type': 'image/png'}

]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'de'
PWA_SERVICE_WORKER_PATH = BASE_DIR / 'static/js/service-worker.js'

# CSP
CSP_DEFAULT_SRC = ("'self'", "https://www.googletagmanager.com")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com")
CSP_IMG_SRC = ("'self'", "data:", "https://*.tile.openstreetmap.org")

# ========== HEROKU ==========
if 'DYNO' in os.environ:
    import django_heroku

    django_heroku.settings(
        locals(),
        staticfiles=False,
        allowed_hosts=False,
        logging=False
    )
    SECURE_SSL_REDIRECT = False

    # Отключаем консольные логи в production
    if not DEBUG:
        for logger_config in LOGGING['loggers'].values():
            if 'console' in logger_config['handlers']:
                logger_config['handlers'].remove('console')
        logger.info("Console logging disabled on Heroku production")
# ============================

logger.info(f"Application started in DEBUG={DEBUG} mode")