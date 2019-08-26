"""Compatibity between Python versions."""
import re
import sys

PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3

if PY2:
    SETTLEMENT_BANK_REFERENCE_REGEX = re.compile(r'^\d{4,7}\.\d{4}\.\d{2}$')
elif PY3:
    SETTLEMENT_BANK_REFERENCE_REGEX = re.compile(r'^\d{4,7}\.\d{4}\.\d{2}$', re.ASCII)
