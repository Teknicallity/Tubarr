import os
from django.core.management.utils import get_random_secret_key

from .base import BASE_DIR, DATABASES

try:
    with open(os.path.join(BASE_DIR, "data", "secretkey.txt")) as f:  # TODO
        SECRET_KEY = f.read().strip()
except:
    SECRET_KEY = get_random_secret_key()

DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} [{levelname}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
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
        'videomanager': {
            'handlers': ['console'],
            'level': os.getenv('TUBARR_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'huey': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        }
    },
}
