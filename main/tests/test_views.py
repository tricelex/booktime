from decimal import Decimal
from unittest.mock import patch

from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from main import forms, models


class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "BookTime")

    def test_about_us_page_works(self):
        response = self.client.get(reverse("about_us"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about_us.html")
        self.assertContains(response, "BookTime")

    def test_contact_us_page_works(self):
        response = self.client.get(reverse("contact_us"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact_form.html")
        self.assertContains(response, "BookTime")
        self.assertIsInstance(response.context["form"], forms.ContactForm)

    def test_products_page_returns_active(self):
        models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        models.Product.objects.create(
            name="A Tale of Two Cities",
            slug="tale-of-two-cities",
            price=Decimal("2.00"),
            active=False,
        )
        response = self.client.get(reverse("products", kwargs={"tag": "all"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BookTime")

        product_list = models.Product.objects.active().order_by("name")

        self.assertEqual(
            list(response.context["object_list"]),
            list(product_list),
        )

    def test_products_page_filters_by_tags_and_active(self):
        cb = models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        cb.tags.create(name="Open source", slug="opensource")
        models.Product.objects.create(
            name="Microsoft Windows guide",
            slug="microsoft-windows-guide",
            price=Decimal("12.00"),
        )
        response = self.client.get(reverse("products", kwargs={"tag": "opensource"}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BookTime")

        product_list = (
            models.Product.objects.active()
            .filter(tags__slug="opensource")
            .order_by("name")
        )

        self.assertEqual(
            list(response.context["object_list"]),
            list(product_list),
        )

    def test_user_signup_page_loads_correctly(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertContains(response, "BookTime")
        self.assertIsInstance(response.context["form"], forms.UserCreationForm)

    def test_user_signup_page_submission_works(self):
        post_data = {
            "email": "user@domain.com",
            "password1": "abcabcabc",
            "password2": "abcabcabc",
        }

        with patch.object(forms.UserCreationForm, "send_mail") as mock_send:
            response = self.client.post(reverse("signup"), post_data)
            print(response)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.User.objects.filter(email="user@domain.com").exists())
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        mock_send.assert_called_once()

    def test_address_list_page_only_returns_owned(self):
        user1 = models.User.objects.create_user("user1", "abcabcabc")
        user2 = models.User.objects.create_user("user2", "abcabcabc")
        models.Address.objects.create(
            user=user1,
            name="jon snow",
            address1="flat 1",
            address2="room 2 1",
            city="ikeja",
            country="uk",
        )
        models.Address.objects.create(
            user=user2,
            name="Mary sue",
            address1="jab 1",
            address2="room 2",
            city="jos",
            country="uk",
        )
        self.client.force_login(user2)
        response = self.client.get(reverse("address_list"))
        self.assertEqual(response.status_code, 200)

        address_list = models.Address.objects.filter(user=user2)
        self.assertEqual(list(response.context["object_list"]), list(address_list))

    def test_address_create_stores_user(self):
        user1 = models.User.objects.create_user("user1", "abcabcabc")
        post_data = {
            "name": "John koddy",
            "address1": "1 apple road",
            "address2": "",
            "zip_code": "MAG78H",
            "city": "Manchester",
            "country": "uk",
        }
        self.client.force_login(user1)
        self.client.post(reverse("address_create"), post_data)
        self.assertTrue(models.Address.objects.filter(user=user1).exists())

    def test_add_to_basket_loggedin_works(self):
        user1 = models.User.objects.create_user("user@me.com", "abcbcdabc")

        cb = models.Product.objects.create(
            name="The Sword",
            slug="the-sword",
            price=Decimal("10.00"),
        )
        w = models.Product.objects.create(
            name="The Cult",
            slug="the-cult",
            price=Decimal("14.00"),
        )
        self.client.force_login(user1)
        response = self.client.get(reverse("add_to_basket"), {"product_id": cb.id})
        response = self.client.get(reverse("add_to_basket"), {"product_id": cb.id})
        self.assertTrue(models.Basket.objects.filter(user=user1).exists())
        self.assertEquals(
            models.BasketLine.objects.filter(basket__user=user1).count(), 1
        )
        response = self.client.get(reverse("add_to_basket"), {"product_id": w.id})
        self.assertEquals(
            models.BasketLine.objects.filter(basket__user=user1).count(), 2
        )
