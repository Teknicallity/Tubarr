import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c#qedy6a&m&&n*t9%y$jp=5wtr&)i-q-kyaizfb9$v9t^knbvt'

DEBUG = False

DEMO_MODE = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'videomanager.apps.VideomanagerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_huey',
    'rest_framework',
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

ROOT_URLCONF = 'Tubarr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'Tubarr.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'config' / 'tubarr.db',
    },
    'tasks': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'config' / 'tasks.db',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CONFIG_DIR = BASE_DIR / 'config'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'content/'

DEMO_DIR = os.path.join(BASE_DIR, 'Tubarr', 'demo_resources')

DJANGO_HUEY = {
    'default': 'download',  # this name must match with any of the queues defined below.
    'queues': {
        'download': {  # this name will be used in decorators below
            'huey_class': 'huey.SqliteHuey',
            'filename': DATABASES['tasks']['NAME'],
            'immediate': False,
            'results': False,
            'store_none': False,
            'consumer': {
                'workers': 1,  # change to environment variable?
                'worker_type': 'thread',
                'health_check_interval': 2,
            },
        },
    }
}

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'drf_link_header_pagination.LinkHeaderPagination',
    'DEFAULT_PAGINATION_CLASS': 'Tubarr.pagination.CustomPagination',
    'PAGE_SIZE': 10
}
