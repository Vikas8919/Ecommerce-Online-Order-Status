from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    if not items:
        return redirect('product_list')

    total = sum(item.total_price() for item in items)

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status="Paid"
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

            # reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        items.delete()  # clear cart

        return redirect('order_success', order_id=order.id)

    return render(request, 'orders/checkout.html', {'items': items, 'total': total})


@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'orders/success.html', {'order': order})

@login_required
def order_status(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'orders/status.html', {'orders': orders})

def payment_method(request):
    # Just show payment options
    if request.method == "POST":
        method = request.POST.get("payment_method")

        if method == "upi":
            return redirect("upi_payment")
        else:
            # For now, directly go to success / checkout
            return redirect("checkout")

    return render(request, "accounts/payment_method.html")


def upi_payment(request):
    # Just show UPI page
    if request.method == "POST":
        # After entering UPI ID → go to success / checkout
        return redirect("checkout")

    return render(request, "upi_payment.html")
