from django.test import SimpleTestCase, Client
from django.urls import reverse
from unittest import mock
from unittest.mock import patch, mock_open
from django.http import HttpResponse
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
    
    @patch('mainapp.views.tempfile.gettempdir', return_value='/mock')
    @patch('mainapp.views.os.path.exists', return_value=True)
    @patch('mainapp.views.os.path.join', return_value='/mock/outputfile.txt')
    @patch('mainapp.views.os.remove')
    @patch('mainapp.views.tempfile.NamedTemporaryFile')
    @patch('builtins.open', new_callable=mock_open, read_data='processed content')
    @patch('mainapp.utils.file_operations.FileReaderDecorator.read', return_value='processed content')
    def test_file_upload_and_download(self, mock_read, mock_open_file, mock_tempfile, mock_remove, mock_path_join, mock_path_exists, mock_gettempdir):
        mock_tempfile.return_value.__enter__.return_value.name = '/mock/tempfile'
        
        mock_file = mock.Mock()
        mock_file.name = 'test.txt'
        mock_file.chunks.return_value = [b'file content']
    
        url = reverse('file_upload')
        response = self.client.post(url, {'file': mock_file, 'output_file': 'outputfile'}, format='multipart')

       
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="outputfile.txt"')
        self.assertEqual(response.content.decode(), 'processed content')

        mock_remove.assert_any_call('/mock/tempfile')
        mock_remove.assert_any_call('/mock/outputfile.txt')


