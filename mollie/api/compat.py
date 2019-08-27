"""Compatibity between Python versions."""
import re
import sys

PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3


def compile_ascii(pattern):
    if PY2:
        return re.compile(pattern)
    elif PY3:
        return re.compile(pattern, re.ASCII)


if PY2:
    from urllib import urlencode
elif PY3:
    from urllib.parse import urlencode
