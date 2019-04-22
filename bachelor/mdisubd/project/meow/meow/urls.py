from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url('^', include('meow_auth.urls')),
    url('^', include('meow_areas.urls')),
    url('^', include('meow_contracts.urls')),
    url('^', include('meow_main.urls')),
]
