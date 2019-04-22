# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework.viewsets import (
    GenericViewSet as BaseGenericViewSet,
    ModelViewSet as BaseModelViewSet, ReadOnlyModelViewSet as BaseReadOnlyModelViewSet
)

from core.api.generic.mixins import FieldsViewMixin, FilteringViewMixin, OrderingViewMixin
from core.api.generic.permissions import JupiterPermission
from jupiter_auth.authentication import TokenAuthentication


class GenericViewSet(FieldsViewMixin,
                     OrderingViewMixin,
                     FilteringViewMixin,
                     BaseGenericViewSet):
    permission_classes = (JupiterPermission,)


class ModelViewSet(BaseModelViewSet, GenericViewSet):
    authentication_classes = [TokenAuthentication]


class ReadOnlyModelViewSet(BaseReadOnlyModelViewSet, GenericViewSet):
    authentication_classes = []
    permission_classes = []
