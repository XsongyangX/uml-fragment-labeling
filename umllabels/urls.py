"""umllabels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from .views import index, validation, get_form
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('labeling/', include(('labeling.urls', 'labeling'), namespace="labeling")),
    path('admin/', admin.site.urls, name='admin'),
    path('', index),
    path('validation/', validation, name='validation'),
    path('validation/form/<str:model>/<slug:kind>/<int:number>', get_form)
    # path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]
