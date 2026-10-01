from django.test import TestCase, Client
from django.urls import reverse
from .models import Argument, PhilosophyCategory, PhilosophyTag

class PhilosophyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = PhilosophyCategory.objects.create(
            name="Metaphysics",
            slug="metaphysics"
        )
        self.tag_ethics = PhilosophyTag.objects.create(
            name="Ethics",
            slug="ethics"
        )
        self.tag_freewill = PhilosophyTag.objects.create(
            name="Free Will",
            slug="free-will"
        )
        self.argument = Argument.objects.create(
            title="On the Bounds of Computational Perception",
            slug="on-the-bounds-of-computational-perception",
            category=self.category,
            thesis="Perception requires an observer bound by thermodynamic constraints.",
            content="## Premise 1\nAny system that perceives must expend energy.\n\n## Conclusion\nUnbounded awareness is non-physical."
        )
        self.argument.tags.add(self.tag_ethics, self.tag_freewill)

    def test_argument_str(self):
        self.assertIn("On the Bounds of Computational Perception", str(self.argument))

    def test_list_view_and_filtering(self):
        response = self.client.get(reverse('philosophy:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "On the Bounds of Computational Perception")
        self.assertContains(response, "Metaphysics")

        filtered_res = self.client.get(reverse('philosophy:list') + '?category=metaphysics')
        self.assertEqual(filtered_res.status_code, 200)
        self.assertContains(filtered_res, "On the Bounds of Computational Perception")

    def test_tag_filtering(self):
        res = self.client.get(reverse('philosophy:list') + '?tag=ethics')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "On the Bounds of Computational Perception")
        self.assertContains(res, "Ethics")

    def test_search_filtering(self):
        # Search by word in thesis
        res = self.client.get(reverse('philosophy:list') + '?q=thermodynamic')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "On the Bounds of Computational Perception")

        # Search by tag name
        res_tag = self.client.get(reverse('philosophy:list') + '?q=Free+Will')
        self.assertEqual(res_tag.status_code, 200)
        self.assertContains(res_tag, "On the Bounds of Computational Perception")

        # Negative search
        res_none = self.client.get(reverse('philosophy:list') + '?q=nonexistentkeyword')
        self.assertEqual(res_none.status_code, 200)
        self.assertNotContains(res_none, "On the Bounds of Computational Perception")

    def test_detail_view(self):
        response = self.client.get(reverse('philosophy:detail', kwargs={'slug': self.argument.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Perception requires an observer")
        self.assertContains(response, "schema.org")
        self.assertContains(response, "Premise 1")
        self.assertContains(response, "Ethics")
