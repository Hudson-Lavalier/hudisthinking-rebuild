from django.test import TestCase, Client
from django.urls import reverse
from .models import Argument

class PhilosophyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.argument = Argument.objects.create(
            title="On the Bounds of Computational Perception",
            slug="on-the-bounds-of-computational-perception",
            category="argument",
            thesis="Perception requires an observer bound by thermodynamic constraints.",
            content="## Premise 1\nAny system that perceives must expend energy.\n\n## Conclusion\nUnbounded awareness is non-physical."
        )

    def test_argument_str(self):
        self.assertIn("On the Bounds of Computational Perception", str(self.argument))

    def test_list_view(self):
        response = self.client.get(reverse('philosophy:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "On the Bounds of Computational Perception")

    def test_detail_view(self):
        response = self.client.get(reverse('philosophy:detail', kwargs={'slug': self.argument.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Perception requires an observer")
        self.assertContains(response, "schema.org")
        self.assertContains(response, "Premise 1")
