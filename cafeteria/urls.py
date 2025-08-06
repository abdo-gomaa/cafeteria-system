from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu'),
    path('order/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/add/', views.add_to_order, name='add_to_order'),
    path('order/<int:order_id>/check-time/', views.check_add_time, name='check_add_time'),
]