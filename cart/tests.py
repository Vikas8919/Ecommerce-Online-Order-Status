from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Category, Product
from .models import Cart, CartItem

class CartTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            description="Test laptop",
            price=50000,
            stock=10
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse("add_to_cart", args=[self.product.id]), {
            "quantity": 2
        })

        cart = Cart.objects.get(user=self.user)
        item = CartItem.objects.get(cart=cart, product=self.product)

        self.assertEqual(item.quantity, 2)

    def test_view_cart(self):
        self.client.post(reverse("add_to_cart", args=[self.product.id]), {"quantity": 1})
        response = self.client.get(reverse("view_cart"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")

    def test_remove_from_cart(self):
        self.client.post(reverse("add_to_cart", args=[self.product.id]), {"quantity": 1})
        cart = Cart.objects.get(user=self.user)
        item = CartItem.objects.get(cart=cart)

        self.client.get(reverse("remove_from_cart", args=[item.id]))
        self.assertEqual(CartItem.objects.count(), 0)
