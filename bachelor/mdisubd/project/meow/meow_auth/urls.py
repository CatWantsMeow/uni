from django.conf.urls import url
from meow_auth.views import LoginView, LandlordRegistrationView, TenantRegistrationView, LogoutView

urlpatterns = [
    url(r'^in/?$', LoginView.as_view(), name='login'),
    url(r'^landlord/up/?$', LandlordRegistrationView.as_view(), name='landlord-registration'),
    url(r'^tenant/up/?$', TenantRegistrationView.as_view(), name='tenant-registration'),
    url(r'^out/?$', LogoutView.as_view(), name='logout'),
]
