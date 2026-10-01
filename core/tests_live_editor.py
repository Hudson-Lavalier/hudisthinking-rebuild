import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from philosophy.models import Argument
from core.models import CustomPage

class LiveEditorApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff_test',
            password='secret_password_123',
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username='normal_test',
            password='secret_password_123',
            is_staff=False
        )
        self.argument = Argument.objects.create(
            title="Initial Test Argument Title",
            slug="initial-test-argument-title",
            content="Initial test content in markdown."
        )
        self.custom_page = CustomPage.objects.create(
            title="Initial Custom Page",
            slug="initial-custom-page",
            content="Initial custom page content."
        )

    def test_anonymous_user_rejected(self):
        payload = {
            'model': 'philosophy.argument',
            'id': self.argument.id,
            'fields': {'title': 'Hacked Title'}
        }
        res = self.client.post(
            '/api/live-editor/save/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 403)
        self.argument.refresh_from_db()
        self.assertEqual(self.argument.title, "Initial Test Argument Title")

    def test_non_staff_user_rejected(self):
        self.client.login(username='normal_test', password='secret_password_123')
        payload = {
            'model': 'philosophy.argument',
            'id': self.argument.id,
            'fields': {'title': 'Hacked Title'}
        }
        res = self.client.post(
            '/api/live-editor/save/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 403)

    def test_staff_user_can_save_argument(self):
        self.client.login(username='staff_test', password='secret_password_123')
        payload = {
            'model': 'philosophy.argument',
            'id': self.argument.id,
            'fields': {
                'title': 'Updated Title Via Live Editor',
                'content': 'Updated content body with **bold** text.'
            }
        }
        res = self.client.post(
            '/api/live-editor/save/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('<strong>bold</strong>', data['rendered_previews']['content'])

        self.argument.refresh_from_db()
        self.assertEqual(self.argument.title, 'Updated Title Via Live Editor')
        self.assertEqual(self.argument.content, 'Updated content body with **bold** text.')

    def test_unauthorized_field_rejected(self):
        self.client.login(username='staff_test', password='secret_password_123')
        payload = {
            'model': 'philosophy.argument',
            'id': self.argument.id,
            'fields': {
                'id': 9999,  # Disallowed field
                'title': 'Test'
            }
        }
        res = self.client.post(
            '/api/live-editor/save/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn('Unauthorized fields', res.json()['message'])

    def test_staff_can_save_custom_page(self):
        self.client.login(username='staff_test', password='secret_password_123')
        payload = {
            'model': 'core.custompage',
            'id': self.custom_page.id,
            'fields': {
                'title': 'Live Saved Custom Page Title',
                'content': 'New content for custom page.'
            }
        }
        res = self.client.post(
            '/api/live-editor/save/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        self.custom_page.refresh_from_db()
        self.assertEqual(self.custom_page.title, 'Live Saved Custom Page Title')
