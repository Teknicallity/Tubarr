import os

from .base import BASE_DIR, DATABASES

DEBUG = True

DEMO_MODE = True

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
            'level': os.getenv('TUBARR_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        'videomanager.content_handlers': {
            'handlers': ['console'],
            'level': os.getenv('TUBARR_LOG_LEVEL', 'DEBUG'),  # TODO
            'propagate': False,
        },
        'huey': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        }
    },
}
