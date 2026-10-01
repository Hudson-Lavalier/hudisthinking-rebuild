from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import SiteConfiguration, DBTemplate, NavigationItem, CustomPage, AboutPage, MediaItem

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
        dummy_img = SimpleUploadedFile("cover.jpg", b"\xff\xd8\xff\xe0dummyjpgcontent", content_type="image/jpeg")
        CustomPage.objects.create(
            title="Axioms of Thought",
            slug="axioms-of-thought",
            content="## Principle 1\nTruth is foundational.",
            featured_image=dummy_img,
            show_featured_image=True,
            is_published=True
        )
        response = self.client.get(reverse('core:custom_page', kwargs={'slug': 'axioms-of-thought'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Axioms of Thought")
        self.assertContains(response, "Truth is foundational.")
        self.assertContains(response, "featured-media-img")

    def test_media_item_model_and_embeds(self):
        dummy_media = SimpleUploadedFile("diagram.png", b"\x89PNGdummycontent", content_type="image/png")
        item = MediaItem.objects.create(
            title="Cosmological Lattice",
            file=dummy_media,
            media_type="image",
            description="Diagram of cosmic manifold."
        )
        self.assertIn("Cosmological Lattice", str(item))
        self.assertIn("![Cosmological Lattice]", item.markdown_embed)
        self.assertNotEqual(item.file_size_display, "0 B")

