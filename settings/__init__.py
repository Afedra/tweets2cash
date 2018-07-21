# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

__title__ = 'Tweets2Cash'
__version__ = '1.0.0'
__author__ = 'Bartile Kapkusum Emmanuel'
__license__ = ''    #TODO
__copyright__ = 'Copyright 2018 Martne Inc'

# Use 'dev', 'beta', or 'final' as the 4th element to indicate release type.
VERSION = (1, 0, 0, 'dev')

def get_short_version():
    return '%s.%s' % (VERSION[0], VERSION[1])

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    # Append 3rd digit if > 0
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    elif VERSION[3] != 'final':
        version = '%s %s' % (version, VERSION[3])
        if len(VERSION) == 5:
            version = '%s %s' % (version, VERSION[4])
    return version

import os, sys

MIN_PYTHON = 3.4
MIN_PYTHON_RELEASE = 3
MIN_PYTHON_DEV_LEVEL = 4

# check python version
if sys.version_info < (MIN_PYTHON_RELEASE,MIN_PYTHON_DEV_LEVEL,):
    sys.exit('Your host needs to use PYTHON ' + str(MIN_PYTHON) + ' or higher to run this version of Tweets2Cash!')

from .celery import *

try:
    from .local import *
except ImportError:
    from .development import *
