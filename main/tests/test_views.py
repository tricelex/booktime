from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from main import forms, models


class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'BookTime')

    def test_about_us_page_works(self):
        response = self.client.get(reverse("about_us"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_us.html')
        self.assertContains(response, 'BookTime')

    def test_contact_us_page_works(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'BookTime')
        self.assertIsInstance(
            response.context['form'], forms.ContactForm
        )

    def test_products_page_returns_active(self):
        models.Product.objects.create(
            slug='cathedral-bazaar',
            price=Decimal('10.00')
        )
        models.Product.objects.create(
            name='A Tale of Two Cities',
            slug='tale-of-two-cities',
            price=Decimal('2.00'),
            active=False,
        )
        response = self.client.get

