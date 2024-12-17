import unittest
import os
import zipfile
import subprocess
from tempfile import TemporaryDirectory
from mainapp.utils.file_operations import TextFileReader, FileReaderDecorator 
from mainapp.views import encrypt_data, decrypt_data, SIGNATURE  
import rarfile

class TestArchiveOperations(unittest.TestCase):

    def setUp(self):
       
        self.test_file_content = b"Hello, world!"
        self.test_file_name = "test_file.txt"
        self.rar_exe_path = r'C:\Program Files\WinRAR\Rar.exe' 

    def test_zip_archive(self):
        with TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, self.test_file_name)
            zip_file_path = os.path.join(temp_dir, "test_archive.zip")

           
            with open(test_file_path, "wb") as f:
                f.write(self.test_file_content)

          
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                zipf.write(test_file_path, arcname=self.test_file_name)

            
            self.assertTrue(os.path.exists(zip_file_path))
            with zipfile.ZipFile(zip_file_path, 'r') as zipf:
                self.assertIn(self.test_file_name, zipf.namelist())

    def test_unzip_archive(self):
        with TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, self.test_file_name)
            zip_file_path = os.path.join(temp_dir, "test_archive.zip")
            extract_to_path = os.path.join(temp_dir, "extracted")

           
            with open(test_file_path, "wb") as f:
                f.write(self.test_file_content)
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                zipf.write(test_file_path, arcname=self.test_file_name)

           
            with zipfile.ZipFile(zip_file_path, 'r') as zipf:
                zipf.extractall(extract_to_path)

           
            extracted_file_path = os.path.join(extract_to_path, self.test_file_name)
            self.assertTrue(os.path.exists(extracted_file_path))
            with open(extracted_file_path, 'rb') as f:
                content = f.read()
            self.assertEqual(content, self.test_file_content)

    def test_rar_archive(self):
        with TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, self.test_file_name)
            rar_file_path = os.path.join(temp_dir, "test_archive.rar")

           
            with open(test_file_path, "wb") as f:
                f.write(self.test_file_content)

            
            result = subprocess.run([self.rar_exe_path, 'a', rar_file_path, test_file_path], check=True, capture_output=True)
            self.assertEqual(result.returncode, 0)

           
            self.assertTrue(os.path.exists(rar_file_path))

    def test_unrar_archive(self):
        with TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, self.test_file_name)
            rar_file_path = os.path.join(temp_dir, "test_archive.rar")
            extract_to_path = os.path.join(temp_dir, "extracted")

           
            with open(test_file_path, "wb") as f:
                f.write(self.test_file_content)
            subprocess.run([self.rar_exe_path, 'a', rar_file_path, test_file_path], check=True, capture_output=True)

            with rarfile.RarFile(rar_file_path) as rar: 
                rar.extractall(extract_to_path)
           

            extracted_file_path = os.path.join(extract_to_path, self.test_file_name)
            self.assertTrue(os.path.exists(extracted_file_path))
            with open(extracted_file_path, 'rb') as f:
                content = f.read()
            self.assertEqual(content, self.test_file_content)

if __name__ == '__main__':
    unittest.main()

