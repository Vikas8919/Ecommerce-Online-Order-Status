from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from orders.models import Order

@login_required
def payment_type(request, order_id):
    order = get_object_or_404(Order, id = order_id, user = request.user)
    return render(request, 'payment/payment_method.html', {"order":order})

@login_required
def upi_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user = request.user)

    if request.method == "POST":
        upi_id = request.POST.get("upi_id")

        order.status= "Paid"
        order.save()

    return render(request, 'payment/upi_payment.html',{"order":order})

