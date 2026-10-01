from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Project

class ProjectsTests(TestCase):
    def setUp(self):
        self.client = Client()
        dummy_file = SimpleUploadedFile("demo_game.zip", b"PK\x03\x04dummycontent")
        self.project = Project.objects.create(
            title="Void Protocol",
            slug="void-protocol",
            project_type="game",
            tagline="An experimental atmospheric game prototype.",
            description="Controls: WASD to move. Space to interact.",
            version="0.1.0",
            platform="Windows x64",
            download_file=dummy_file
        )

    def test_project_str(self):
        self.assertIn("Void Protocol", str(self.project))

    def test_list_view(self):
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Void Protocol")

    def test_detail_view(self):
        response = self.client.get(reverse('projects:detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SoftwareApplication")
        self.assertContains(response, self.project.filename)
        self.assertContains(response, "WASD to move")
