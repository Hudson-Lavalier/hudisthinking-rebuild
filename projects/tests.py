from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Project, ProjectCategory

class ProjectsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ProjectCategory.objects.create(
            name="Standalone Executables",
            slug="standalone-executables"
        )
        dummy_file = SimpleUploadedFile("demo_game.zip", b"PK\x03\x04dummycontent")
        self.project = Project.objects.create(
            title="Void Protocol",
            slug="void-protocol",
            project_type=self.category,
            tagline="An experimental atmospheric game prototype.",
            description="Controls: WASD to move. Space to interact.",
            version="0.1.0",
            platform="Windows x64",
            download_file=dummy_file
        )

    def test_project_str(self):
        self.assertIn("Void Protocol", str(self.project))

    def test_list_view_and_filtering(self):
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Void Protocol")
        self.assertContains(response, "Standalone Executables")

        filtered_res = self.client.get(reverse('projects:list') + '?type=standalone-executables')
        self.assertEqual(filtered_res.status_code, 200)
        self.assertContains(filtered_res, "Void Protocol")

    def test_detail_view(self):
        response = self.client.get(reverse('projects:detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SoftwareApplication")
        self.assertContains(response, self.project.filename)
        self.assertContains(response, "WASD to move")
