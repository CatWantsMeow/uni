# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .db import *
from .django import *
from .logging import *
from .mail import *
from .rest_framework import *

if 'test' in sys.argv:
    from .test_settings import *
