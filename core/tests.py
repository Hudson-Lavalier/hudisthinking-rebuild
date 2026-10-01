from django.test import TestCase, Client
from django.urls import reverse
from .models import SiteConfiguration, DBTemplate, NavigationItem, CustomPage, AboutPage

class MetaEditabilityTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_default_template_renders_from_filesystem(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HudIsThinking")

    def test_dbtemplate_overrides_filesystem(self):
        # Create an override for home.html in DB
        DBTemplate.objects.create(
            name="home.html",
            content="{% extends 'base.html' %}{% block content %}<h1>CUSTOM DB HOMEPAGE OVERRIDE</h1>{% endblock %}",
            is_active=True
        )
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CUSTOM DB HOMEPAGE OVERRIDE")

    def test_dbtemplate_deactivation_falls_back_to_filesystem(self):
        dbt = DBTemplate.objects.create(
            name="home.html",
            content="{% extends 'base.html' %}{% block content %}<h1>CUSTOM DB HOMEPAGE OVERRIDE</h1>{% endblock %}",
            is_active=False
        )
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "CUSTOM DB HOMEPAGE OVERRIDE")
        self.assertContains(response, "Philosophy & Arguments")

    def test_site_configuration_custom_css_injection(self):
        config = SiteConfiguration.get_solo()
        config.custom_css = "body { letter-spacing: 0.15em; }"
        config.save()

        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "letter-spacing: 0.15em;")

    def test_navigation_items_render_in_header(self):
        NavigationItem.objects.create(
            label="Manifesto",
            url="/page/manifesto/",
            location="header",
            order=10,
            is_active=True
        )
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manifesto")

    def test_custom_page_rendering(self):
        CustomPage.objects.create(
            title="Axioms of Thought",
            slug="axioms-of-thought",
            content="## Principle 1\nTruth is foundational.",
            is_published=True
        )
        response = self.client.get(reverse('core:custom_page', kwargs={'slug': 'axioms-of-thought'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Axioms of Thought")
        self.assertContains(response, "Truth is foundational.")
