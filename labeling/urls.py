from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

from . import views

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
    path('', views.IndexView.as_view(), name='index'),
]