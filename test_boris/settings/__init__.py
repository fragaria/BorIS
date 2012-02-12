try:
    from boris.settings import *
except ImportError:
    pass

try:
    from base import *
except ImportError:
    pass

try:
    from local import *
except ImportError:
    pass
