# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from django.core.management import BaseCommand

from finance.fixtures import init_credit_templates

logger = logging.getLogger('jupiter')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        logger.info('Initializing credits templates...')
        init_credit_templates()
        logger.info('Initializing credits templates complete')
