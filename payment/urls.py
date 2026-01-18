from django.urls import path
from . import views

urlpatterns = [
    path('payment_gateway/<int:order_id>/',views.payment_type,name="gateway"),
    path('upi_payment/<int:order_id>/',views.upi_payment,name="upi"),

]
