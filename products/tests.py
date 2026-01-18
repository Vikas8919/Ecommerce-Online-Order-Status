from django.test import TestCase
from django.urls import reverse
from .models import Category, Product

class ProductTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Mobile",
            description="Smart phone",
            price=10000,
            stock=5,
            is_available=True
        )

    def test_product_created(self):
        self.assertEqual(self.product.name, "Mobile")
        self.assertEqual(self.product.stock, 5)

    def test_product_list_view(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mobile")

    def test_product_detail_view(self):
        response = self.client.get(reverse("product_detail", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smart phone")
