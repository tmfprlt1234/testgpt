import base64
import os
from pathlib import Path
from urllib.parse import unquote, urlparse

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


PG_ENV_KEYS = [
    'PGDATABASE',
    'PGHOST',
    'PGHOSTADDR',
    'PGPORT',
    'PGUSER',
    'PGPASSWORD',
    'PGPASSFILE',
    'PGSERVICE',
    'PGSERVICEFILE',
    'PGOPTIONS',
    'PGSSLMODE',
]


def load_env_file() -> None:
    env_path = BASE_DIR / '.env'
    if not env_path.exists():
        return

    try:
        load_dotenv(env_path, encoding='utf-8-sig', override=False)
    except UnicodeDecodeError:
        load_dotenv(env_path, encoding='cp949', override=False)


def clean_env(name: str, default: str = '') -> str:
    value = os.getenv(name, default)
    if value is None:
        return default
    cleaned = value.strip().strip('"').strip("'")
    return cleaned.lstrip('\ufeff')


def parse_password() -> str:
    encoded = clean_env('POSTGRES_PASSWORD_B64', '')
    if encoded:
        return base64.b64decode(encoded).decode('utf-8')
    return clean_env('POSTGRES_PASSWORD', 'postgres')


def clear_conflicting_pg_env() -> None:
    """Avoid libpq using unexpected system-level PG* variables on Windows shells."""
    for key in PG_ENV_KEYS:
        if key == 'PGCLIENTENCODING':
            continue
        if key in os.environ:
            os.environ.pop(key, None)


def postgres_database_options() -> dict:
    options = {
        'client_encoding': clean_env('PGCLIENTENCODING', 'UTF8'),
        'connect_timeout': int(clean_env('POSTGRES_CONNECT_TIMEOUT', '10')),
        'options': clean_env('POSTGRES_OPTIONS', '-c client_encoding=UTF8'),
    }

    # Only pass service/passfile when explicitly enabled and non-empty.
    if clean_env('POSTGRES_DISABLE_PGSERVICE', 'True').lower() != 'true':
        service = clean_env('POSTGRES_SERVICE', '')
        if service:
            options['service'] = service

    if clean_env('POSTGRES_DISABLE_PGPASSFILE', 'True').lower() != 'true':
        passfile = clean_env('POSTGRES_PASSFILE', '')
        if passfile:
            options['passfile'] = passfile

    return options


def postgres_database_config() -> dict:
    database_url = clean_env('DATABASE_URL', '')
    if database_url:
        parsed = urlparse(database_url)
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': unquote(parsed.path.lstrip('/')) or 'company_data',
            'USER': unquote(parsed.username or 'postgres'),
            'PASSWORD': unquote(parsed.password or 'postgres'),
            'HOST': parsed.hostname or 'localhost',
            'PORT': str(parsed.port or '5432'),
            'OPTIONS': postgres_database_options(),
        }

    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': clean_env('POSTGRES_DB', 'company_data'),
        'USER': clean_env('POSTGRES_USER', 'postgres'),
        'PASSWORD': parse_password(),
        'HOST': clean_env('POSTGRES_HOST', 'localhost'),
        'PORT': clean_env('POSTGRES_PORT', '5432'),
        'OPTIONS': postgres_database_options(),
    }


load_env_file()
os.environ.setdefault('PGCLIENTENCODING', clean_env('PGCLIENTENCODING', 'UTF8'))
clear_conflicting_pg_env()

SECRET_KEY = clean_env('DJANGO_SECRET_KEY', 'change-me-in-production')
DEBUG = clean_env('DJANGO_DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = [h.strip() for h in clean_env('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'records',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

if clean_env('USE_SQLITE', 'False').lower() == 'true':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': postgres_database_config(),
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
