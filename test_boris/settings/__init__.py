try:
    from boris.settings import *
except ImportError:
    pass

try:
    from test_boris.settings.base import *
except ImportError:
    pass

try:
    from test_boris.settings.local import *
except ImportError:
    pass
