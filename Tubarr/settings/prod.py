import os, logging
from django.core.management.utils import get_random_secret_key

from .base import BASE_DIR, CONFIG_DIR

logger = logging.getLogger(__name__)

try:
    with open(os.path.join(CONFIG_DIR, "secretkey.txt")) as f:
        SECRET_KEY = f.read().strip()
except FileNotFoundError:
    SECRET_KEY = get_random_secret_key()
    try:
        with open(os.path.join(CONFIG_DIR, "secretkey.txt"), 'w') as f:
            f.write(SECRET_KEY)
    except FileNotFoundError as e:
        logger.warning("Directory does not exist; unable to write secret key: %s", e)
    except OSError as e:
        logger.warning("Error writing secret key to file: %s", e)

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

DEMO_MODE = os.getenv('DEMO_MODE', 'False').lower() == 'true'

CSRF_TRUSTED_ORIGINS = (
    os.getenv("CSRF_TRUSTED_ORIGINS", "")
    .split(",") if os.getenv("CSRF_TRUSTED_ORIGINS", "").strip() else []
)

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
