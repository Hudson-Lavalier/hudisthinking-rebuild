from django.test import TestCase, Client
from django.urls import reverse
from .models import AboutPage

class CoreTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HudIsThinking")
        self.assertContains(response, "Philosophy & Arguments")
        self.assertContains(response, "Projects & Software")

    def test_about_view_default(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HudIsThinking LLC")

    def test_about_view_custom_content(self):
        AboutPage.objects.create(
            title="About HudIsThinking",
            content="Official studio and archive."
        )
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Official studio and archive.")
