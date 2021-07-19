from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/<slug:model>/<slug:kind>/<int:number>', views.get_form)
]