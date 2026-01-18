from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Category, Product
from cart.models import Cart, CartItem
from .models import Order

class OrderTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="orderuser", password="12345")
        self.client.login(username="orderuser", password="12345")

        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Headphones",
            description="Test product",
            price=2000,
            stock=5
        )

        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_checkout(self):
        response = self.client.post(reverse("checkout"))

        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total_amount, 4000)
        self.assertEqual(order.status, "Paid")

    def test_order_success_page(self):
        self.client.post(reverse("checkout"))
        order = Order.objects.get(user=self.user)

        response = self.client.get(reverse("order_success", args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order Placed Successfully")
