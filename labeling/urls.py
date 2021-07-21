from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/<str:model>/<slug:kind>/<int:number>', views.get_form),
    path('specific/<str:model>/<slug:kind>/<int:number>', views.specific, name='specific')
]