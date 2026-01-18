from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('orderstatus/', views.order_status, name='order_status'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
]
