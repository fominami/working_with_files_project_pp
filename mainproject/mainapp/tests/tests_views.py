from django.test import SimpleTestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from ..forms import FileUploadForm
import os

class FileUploadViewTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('file_upload')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'file_upload.html')
        self.assertIsInstance(response.context['form'], FileUploadForm)

    def test_post_txt_file(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'mainapp', 'tests', 'data', 'input.txt')
        if not os.path.exists(file_path):
            self.fail(f"Тестовый файл не найден: {file_path}")
        with open(file_path, 'rb') as upload_file:
            file_data = {'file': SimpleUploadedFile(upload_file.name, upload_file.read())}
            response = self.client.post(self.url, file_data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'file_content', response.content)  
    def test_post_json_file(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'mainapp', 'tests', 'data', 'example.json')
        if not os.path.exists(file_path):
            self.fail(f"Json файл не найден: {file_path}")
        with open(file_path, 'rb') as upload_file:
            file_data = {'file': SimpleUploadedFile(upload_file.name, upload_file.read())}
            response = self.client.post(self.url, file_data)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'file_content', response.content)  
    def test_post_xml_file(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'mainapp', 'tests', 'data', 'example.xml')
        if not os.path.exists(file_path):
            self.fail(f"Xml файл не найден: {file_path}")
        with open(file_path, 'rb') as upload_file:
            file_data = {'file': SimpleUploadedFile(upload_file.name, upload_file.read())}
            response = self.client.post(self.url, file_data)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'file_content', response.content)  
    def test_post_yaml_file(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'mainapp', 'tests', 'data', 'input.yaml')
        if not os.path.exists(file_path):
            self.fail(f"Yaml файл не найден: {file_path}")
        with open(file_path, 'rb') as upload_file:
            file_data = {'file': SimpleUploadedFile(upload_file.name, upload_file.read())}
            response = self.client.post(self.url, file_data)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'file_content', response.content)  

    def test_post_invalid_file_type(self):
        invalid_file = SimpleUploadedFile("test_file.invalid", b"invalid_content")
        response = self.client.post(self.url, {'file': invalid_file})
        
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Unsupported file type.", response.content)

