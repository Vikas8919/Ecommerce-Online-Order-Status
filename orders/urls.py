from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('orderstatus/', views.order_status, name='order_status'),
    path("payment/", views.payment_method, name="payment_method"),
    path("payment/upi/", views.upi_payment, name="upi_payment"),

]
