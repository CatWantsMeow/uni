from django.conf.urls import url
from meow_auth.views import LoginView, LandlordRegistrationView, TenantRegistrationView
from meow_contracts.views import RentRequestCreateView, RentRequestListView, RentContractListView, \
    DeleteRentContractView, StartRentView, EndRentView, RentContractCreateView, DeleteRentRequestView

urlpatterns = [
    url(
        '^rent-contracts/create/(?P<tenant_id>[0-9]+)/(?P<area_id>[0-9]+)/?$',
        RentContractCreateView.as_view(),
        name='rent-contract-create'
    ),

    url(
        '^rent-contracts/(?P<contract_id>[0-9]+)/edit/(?P<tenant_id>[0-9]+)/(?P<area_id>[0-9]+)/?$',
        RentContractCreateView.as_view(),
        name='rent-contract-edit'
    ),

    url(
        '^rent-contracts/(?P<contract_id>[0-9]+)/delete/?$',
        DeleteRentContractView.as_view(),
        name='rent-contract-delete'
    ),

    url(
        '^rent-contracts/(?P<contract_id>[0-9]+)/start-rent/?$',
        StartRentView.as_view(),
        name='rent-contract-start-rent'
    ),

    url(
        '^rent-contracts/(?P<contract_id>[0-9]+)/end-rent/?$',
        EndRentView.as_view(),
        name='rent-contract-end-rent'
    ),

    url(
        '^malls/(?P<mall_id>[0-9]+)/areas/(?P<area_id>[0-9]+)/rent-request/?$',
        RentRequestCreateView.as_view(),
        name='area-rent-request'
    ),

    url(
        '^rent-requests/delete/(?P<tenant_id>[0-9]+)/(?P<area_id>[0-9]+)?$',
        DeleteRentRequestView.as_view(),
        name='rent-request-delete'
    ),

    url(
        '^rent-requests/?$',
        RentRequestListView.as_view(),
        name='rent-request-list'
    ),

    url(
        '^rent-contracts/?$',
        RentContractListView.as_view(),
        name='rent-contract-list'
    )
]

