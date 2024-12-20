import unittest
import os
import zipfile
import rarfile
import subprocess
import tempfile
from mainapp.utils.strategy_archive import ZipArchiveStrategy, RarArchiveStrategy, EncryptStrategy, FileProcessorContext
from mainapp.utils.file_operations import FileReaderDecorator
from mainapp.utils.encryption import SIGNATURE, encrypt_data, decrypt_data

class TestArchiveOperations(unittest.TestCase):

    def setUp(self):
        self.test_file_content = b"Hello, world!"
        self.test_file_name = "test_file.txt"
        self.rar_exe_path = r'C:\Program Files\WinRAR\Rar.exe'
        self.context = FileProcessorContext(None)

    def test_zip_archive(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, self.test_file_name)
            zip_file_path = os.path.join(temp_dir, "test_archive.zip")
            
            with open(test_file_path, "wb") as f:
                f.write(self.test_file_content)
                
            strategy = ZipArchiveStrategy()
            self.context.set_strategy(strategy)
            self.context.execute_strategy(test_file_path, zip_file_path)

            self.assertTrue(os.path.exists(zip_file_path))
            with zipfile.ZipFile(zip_file_path, 'r') as zipf:
                self.assertIn(self.test_file_name, zipf.namelist())

    def test_unzip_archive(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, self.test_file_name)
            zip_file_path = os.path.join(temp_dir, "test_archive.zip")
            extract_to_path = os.path.join(temp_dir, "extracted")

            with open(test_file_path, "wb") as f:
                f.write(self.test_file_content)
            strategy = ZipArchiveStrategy()
            self.context.set_strategy(strategy)
            self.context.execute_strategy(test_file_path, zip_file_path)

            with zipfile.ZipFile(zip_file_path, 'r') as zipf:
                zipf.extractall(extract_to_path)

            extracted_file_path = os.path.join(extract_to_path, self.test_file_name)
            self.assertTrue(os.path.exists(extracted_file_path))
            with open(extracted_file_path, 'rb') as f:
                content = f.read()
            self.assertEqual(content, self.test_file_content)

    def test_rar_archive(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, self.test_file_name)
            rar_file_path = os.path.join(temp_dir, "test_archive.rar")

            with open(test_file_path, "wb") as f:
                f.write(self.test_file_content)

            strategy = RarArchiveStrategy(self.rar_exe_path)
            rar_file_path = os.path.join(tempfile.gettempdir(), f"test_file.rar") 
            self.context.set_strategy(strategy)
            self.context.execute_strategy(test_file_path, rar_file_path)

            self.assertTrue(os.path.exists(rar_file_path))
            with rarfile.RarFile(rar_file_path) as rar:
               file_names = [os.path.basename(info.filename) for info in rar.infolist()] 
               self.assertIn(self.test_file_name, file_names)
    def test_unrar_archive(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, self.test_file_name)
            rar_file_path = os.path.join(temp_dir, "test_archive.rar")
            extract_to_path = os.path.join(temp_dir, "extracted")

            with open(test_file_path, "wb") as f:
                f.write(self.test_file_content)
            strategy = RarArchiveStrategy(self.rar_exe_path)
            self.context.set_strategy(strategy)
            self.context.execute_strategy(test_file_path, rar_file_path)
            reader = FileReaderDecorator(None) 
            reader.set_file_path(rar_file_path) 
            extracted_file_path = reader.extract_rar(rar_file_path, extract_to_path) 
            self.assertTrue(os.path.exists(extracted_file_path)) 
            with open(extracted_file_path, 'rb') as f: 
                content = f.read() 
            self.assertEqual(content, self.test_file_content)

### Шаг 2: Создание тестов для шифрования и дешифровки

    def test_encrypt(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, self.test_file_name)
            enc_file_path = os.path.join(temp_dir, "test_encrypted.enc")

            with open(test_file_path, "wb") as f:
                f.write(self.test_file_content)

            strategy = EncryptStrategy()
            self.context.set_strategy(strategy)
            self.context.execute_strategy(test_file_path, enc_file_path)

            self.assertTrue(os.path.exists(enc_file_path))
            with open(enc_file_path, 'rb') as f:
                content = f.read()
            self.assertTrue(content.startswith(SIGNATURE))
            decrypted_data = decrypt_data(content[len(SIGNATURE):])
            self.assertEqual(decrypted_data, self.test_file_content)

    def test_decrypt(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, self.test_file_name)
            enc_file_path = os.path.join(temp_dir, "test_encrypted.enc")

            with open(test_file_path, "wb") as f:
                f.write(self.test_file_content)

            strategy = EncryptStrategy()
            self.context.set_strategy(strategy)
            self.context.execute_strategy(test_file_path, enc_file_path)

            with open(enc_file_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = decrypt_data(encrypted_data[len(SIGNATURE):])

            decrypted_file_path = os.path.join(temp_dir, "test_decrypted.txt")
            with open(decrypted_file_path, 'wb') as f:
                f.write(decrypted_data)

            self.assertTrue(os.path.exists(decrypted_file_path))
            with open(decrypted_file_path, 'rb') as f:
                content = f.read()
            self.assertEqual(content, self.test_file_content)

if __name__ == '__main__':
    unittest.main()
