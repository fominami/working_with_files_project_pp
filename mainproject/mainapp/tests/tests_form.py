from django.test import SimpleTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from mainapp.forms import FileUploadForm
import os

class FileUploadFormTest(SimpleTestCase):
    def test_valid_txt_form(self):

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'mainapp', 'tests', 'data', 'input.txt')
        if not os.path.exists(file_path):
            self.fail(f"Тестовый файл не найден: {file_path}")
        with open(file_path, 'rb') as upload_file:
            file_data = {'file': SimpleUploadedFile(upload_file.name, upload_file.read())}

            form = FileUploadForm({}, file_data)

            self.assertTrue(form.is_valid())
    def test_valid_json_form(self):

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'mainapp', 'tests', 'data', 'example.json')
        if not os.path.exists(file_path):
            self.fail(f"Json файл не найден: {file_path}")
        with open(file_path, 'rb') as upload_file:
            file_data = {'file': SimpleUploadedFile(upload_file.name, upload_file.read())}

            form = FileUploadForm({}, file_data)

            self.assertTrue(form.is_valid())
    def test_valid_xml_form(self):

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'mainapp', 'tests', 'data', 'example.xml')
        if not os.path.exists(file_path):
            self.fail(f"Xml файл не найден: {file_path}")
        with open(file_path, 'rb') as upload_file:
            file_data = {'file': SimpleUploadedFile(upload_file.name, upload_file.read())}

            form = FileUploadForm({}, file_data)

            self.assertTrue(form.is_valid())
    def test_valid_yaml_form(self):

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'mainapp', 'tests', 'data', 'input.yaml')
        if not os.path.exists(file_path):
            self.fail(f"Yaml файл не найден: {file_path}")
        with open(file_path, 'rb') as upload_file:
            file_data = {'file': SimpleUploadedFile(upload_file.name, upload_file.read())}

            form = FileUploadForm({}, file_data)

            self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = FileUploadForm({}, {})

        self.assertFalse(form.is_valid())
