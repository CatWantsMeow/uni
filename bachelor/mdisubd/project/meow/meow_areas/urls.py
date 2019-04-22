from django.conf.urls import url

from meow_areas.views import ShoppingMallListView, ShoppingMallDetailView, ShoppingMallCreateView, ShoppingMallDeleteView, \
    ShoppingAreaCreateView, ShoppingAreaDeleteView
from meow_auth.views import LoginView, LandlordRegistrationView, TenantRegistrationView

urlpatterns = [
    url(
        '^malls/(?P<mall_id>[0-9]+)/areas/(?P<area_id>[0-9]+)/edit/?$',
        ShoppingAreaCreateView.as_view(), name='area-edit'
    ),
    url(
        '^malls/(?P<mall_id>[0-9]+)/areas/(?P<area_id>[0-9]+)/delete/?$',
        ShoppingAreaDeleteView.as_view(), name='area-delete'
    ),
    url('^malls/(?P<mall_id>[0-9]+)/areas/create/?$', ShoppingAreaCreateView.as_view(), name='area-create'),
    url('^malls/(?P<mall_id>[0-9]+)/delete/?$', ShoppingMallDeleteView.as_view(), name='mall-delete'),
    url('^malls/(?P<mall_id>[0-9]+)/edit/?$', ShoppingMallCreateView.as_view(), name='mall-edit'),
    url('^malls/(?P<mall_id>[0-9]+)/?$', ShoppingMallDetailView.as_view(), name='mall-detail'),
    url('^malls/create/?$', ShoppingMallCreateView.as_view(), name='mall-create'),
    url('^malls/?$', ShoppingMallListView.as_view(), name='mall-list'),
]
