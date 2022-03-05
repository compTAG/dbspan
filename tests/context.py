import sys
import os

libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, libpath)

import dbspan  # noqa # pylint: disable=unused-import, wrong-import-position
