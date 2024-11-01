
import sys

from .base import *
for a in sys.argv:
    print(a)
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    from .test import *
else:
    try:
        from .dev import *
    except:
        from .prod import *
