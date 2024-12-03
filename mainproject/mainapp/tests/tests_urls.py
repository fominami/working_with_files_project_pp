from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mainapp.views import FileUploadView
class TestUrls(SimpleTestCase):
    def test_home_page(self):
        url=reverse('file_upload')
        self.assertEqual(resolve(url).func.view_class, FileUploadView)