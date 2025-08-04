from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu'),
    path('order/', views.place_order, name='place_order'),
]