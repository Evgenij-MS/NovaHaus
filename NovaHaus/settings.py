
"""
Django settings for NovaHaus
"""
from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured

# Basisverzeichnis
BASE_DIR = Path(__file__).resolve().parent.parent

# Hilfsfunktion für Umgebungsvariablen
def get_env_variable(var_name, default=None):
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        raise ImproperlyConfigured(f"Umgebungsvariable {var_name} fehlt.")

# SECURITY
SECRET_KEY = get_env_variable("SECRET_KEY", "dev-key-change-in-production-" + "x" * 50)
DEBUG = get_env_variable("DJANGO_DEBUG", "True").lower() not in ("false", "0", "f", "n", "no")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "novahaus-eu.herokuapp.com",
    "novahaus-koeln.de",
    "www.novahaus-koeln.de",
    "novahaus-hamburg.de",
    "www.novahaus-hamburg.de",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "channels",
    "whitenoise.runserver_nostatic",
    "compressor",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "axes",
    "django_extensions",
    "main",
    "profiles",
    "pwa",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "axes.middleware.AxesMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "NovaHaus.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", BASE_DIR / "main" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
            ],
        },
    },
]

# WSGI / ASGI
WSGI_APPLICATION = "NovaHaus.wsgi.application"
ASGI_APPLICATION = "NovaHaus.asgi.application"

# Datenbank
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# Internationalisierung
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = "Europe/Berlin"
LANGUAGE_CODE = "de"
LANGUAGES = [
    ("de", "Deutsch"),
    ("en", "English"),
    ("tr", "Türkçe"),
    ("ru", "Русский"),
]
LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Sprach-Cookie Einstellungen
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 Tage
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_SECURE = not DEBUG
LANGUAGE_COOKIE_HTTPONLY = False
LANGUAGE_COOKIE_SAMESITE = 'Lax'

# Sessions
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 86400 * 30  # 30 Tage
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Static und Media Dateien
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Sicherheitsoptionen
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

# CSRF Einstellungen
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_AGE = 31449600
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://novahaus-koeln.de",
    "https://www.novahaus-koeln.de",
    "https://novahaus-hamburg.de",
    "https://www.novahaus-hamburg.de",
]

# Authentifizierung
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Django Axes (KORRIGIERTE Einstellungen)
# AXES_FAILURE_LIMIT = 5
# AXES_COOLOFF_TIME = 1  # Stunde
# AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True  # DIESE ZEILE ENTFERNT!
# AXES_RESET_ON_SUCCESS = True
# AXES_LOCKOUT_CALLABLE = 'axes.lockout.database_lockout'

# Django OTP
OTP_TOTP_ISSUER = 'NovaHaus'

# E-Mail Einstellungen
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@novahaus.de'
SERVER_EMAIL = 'server@novahaus.de'

# Progressive Web App
PWA_APP_NAME = "NovaHaus"
PWA_APP_DESCRIPTION = "Renovation services in Cologne and Hamburg"
PWA_APP_THEME_COLOR = "#005B99"
PWA_APP_BACKGROUND_COLOR = "#FFFFFF"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [
    {
        "src": "/static/images/favicon/android-chrome-192x192.png",
        "sizes": "192x192",
        "type": "image/png"
    },
    {
        "src": "/static/images/favicon/android-chrome-512x512.png",
        "sizes": "512x512",
        "type": "image/png"
    },
]
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static', 'js', 'service-worker.js')

# Compressor Einstellungen
COMPRESS_ENABLED = not DEBUG
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# Standard Primary Key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Datei-Upload Einstellungen
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Logging
class UTF8EncodingFilter:
    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = record.msg.encode("utf-8", errors="ignore").decode("utf-8")
        return True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "utf8": {"()": UTF8EncodingFilter},
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["utf8"],
            "formatter": "simple",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "filters": ["utf8"],
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",  # Reduziert INFO-Spam
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "main": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",  # Reduziert Logs
    },
}

# Erstelle logs Verzeichnis
logs_dir = BASE_DIR / "logs"
if not logs_dir.exists():
    logs_dir.mkdir(exist_ok=True)

# Produktionsspezifische Einstellungen
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_TZ = True