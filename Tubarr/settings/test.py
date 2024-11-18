
from .base import DATABASES

DJANGO_HUEY = {
    'default': 'download',  # this name must match with any of the queues defined below.
    'queues': {
        'download': {  # this name will be used in decorators below
            'huey_class': 'huey.MemoryHuey',
            'immediate': True,
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
