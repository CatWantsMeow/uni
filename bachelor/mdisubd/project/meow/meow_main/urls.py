from django.conf.urls import url

from meow_main.views import HomeView

urlpatterns = [
    url(
        '^',
        HomeView.as_view(),
        name='home'
    ),
]