import re
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
_ = lambda s: s

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

def get_env_variable(var_name, default=None):
    value = os.getenv(var_name, default)
    if value is None:
        logging.warning(f"Переменная окружения {var_name} отсутствует, используем значение по умолчанию.")
        return default
    return value

SECRET_KEY = get_env_variable('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't', 'y', 'yes')
ROOT_URLCONF = 'NovaHaus.urls'

ALLOWED_HOSTS = [
    'novahaus-eu.herokuapp.com',
    'novahaus-eu-5b21cc3bb91d.herokuapp.com',
    'novahaus-koeln.de',
    'www.novahaus-koeln.de',
    'novahaus-hamburg.de',
    'www.novahaus-hamburg.de',
    'localhost',
    '127.0.0.1'
]

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
    'pwa',  # Добавлено для PWA
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
]

USE_I18N = True
USE_L10N = True

LANGUAGE_CODE = 'de'  # Основной язык — немецкий
LANGUAGES = [
    ('de', 'Deutsch'),
    ('en', 'English'),
    ('tr', 'Türkçe'),
    ('ru', 'Русский'),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 365 * 24 * 60 * 60  # 1 год

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

ALLOW_CURL = os.getenv("ALLOW_CURL", "False") == "True"

DISALLOWED_USER_AGENTS = [
    re.compile(r'bot'),
    re.compile(r'scanner'),
    re.compile(r'curl'),
    re.compile(r'Chrome/91\.0\.4472\.124'),
    re.compile(r'python-requests'),
    re.compile(r'Go-http-client'),
    re.compile(r'Java/'),
    re.compile(r'nikto'),
    re.compile(r'sqlmap'),
    re.compile(r'wget'),
    re.compile(r'libwww-perl'),
    re.compile(r'zgrab'),
    re.compile(r'okhttp'),
    re.compile(r'postman')
]

if not ALLOW_CURL:
    DISALLOWED_USER_AGENTS.extend([
        re.compile(r'curl'),
        re.compile(r'python-requests'),
    ])

SENSITIVE_URL_PATTERNS = [
    re.compile(r'(^|/)\.env$'),
    re.compile(r'(^|/)wp-'),
    re.compile(r'(^|/)config'),
    re.compile(r'(^|/)backup'),
    re.compile(r'(^|/)\.git$'),
    re.compile(r'\.sql$'),
    re.compile(r'\.bak$'),
    re.compile(r'\.log$'),
    re.compile(r'(^|/)phpmyadmin'),
    re.compile(r'(^|/)docker'),
    re.compile(r'(^|/)npm'),
]

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_LOCKOUT_TEMPLATE = 'errors/lockout.html'
AXES_RESET_ON_SUCCESS = True
AXES_DISABLE_ACCESS_LOG = True

# Настройка базы данных
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'NH',
            'USER': 'postgres',
            'PASSWORD': 'Okro.123',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

OTP_TOTP_ISSUER = 'NovaHaus'

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

COMPRESS_ENABLED = not DEBUG
COMPRESS_OFFLINE = not DEBUG
COMPRESS_CSS_FILTERS = [
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

REDIS_URL = os.getenv('REDISCLOUD_URL', 'redis://localhost:6379/0')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
            'socket_timeout': 5,
        },
    },
}

ASGI_APPLICATION = 'NovaHaus.asgi.application'

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

CACHE_TTL = 60 * 15

import sentry_sdk
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

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
    {
        'src': '/static/images/favicon/favicon-192x192.png',
        'sizes': '192x192',
        'type': 'image/png'
    },
    {
        'src': '/static/images/favicon/favicon-512x512.png',
        'sizes': '512x512',
        'type': 'image/png'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/splash.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'de'