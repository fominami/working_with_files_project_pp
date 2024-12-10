import json
import yaml
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from .data_processing import DataProcessor
import tempfile
import zipfile 
import os

class FileReader(ABC):
    @abstractmethod
    def read(self):
        pass
    @abstractmethod 
    def write(self, content, output_file): 
        pass


class TextFileReader:
    def __init__(self, file_path, encoding='utf-8'):
        self.file_path = file_path
        self.encoding = encoding

    def read(self):
        try:
            with open(self.file_path, 'r', encoding=self.encoding) as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(self.file_path, 'r', encoding='windows-1251') as f:
                content = f.read()
        return content
    def write(self, content, output_file):
        with open(output_file, 'w', encoding=self.encoding) as f: 
            f.write(content)



class JSONFileReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'r') as f:
            content = f.read()
            if not content:
                raise ValueError("Файл пустой")
            json_content = json.loads(content)
        return json.dumps(json_content, indent=4)
    def write(self, content, output_file): 
        with open(output_file, 'w') as f: 
            json.dump(json.loads(content), f, indent=4)


class YAMLFileReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'r') as f:
            try:
                content = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Error reading YAML file: {e}")
        return yaml.dump(content, default_flow_style=False)
    def write(self, content, output_file): 
        with open(output_file, 'w') as f: 
            yaml.dump(yaml.safe_load(content), f, default_flow_style=False)


class XMLFileReader(FileReader):
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return ET.tostring(root, encoding='unicode')
    def write(self, content, output_file): 
        root = ET.ElementTree(ET.fromstring(content)) 
        root.write(output_file, encoding='unicode')

class FileReaderDecorator(FileReader):
    def __init__(self, file_reader):
        self._file_reader = file_reader

    def set_file_path(self, file_path):
        self.file_path = file_path
    def read(self): 
       
        content = self._file_reader.read()
        processed_content = self._process_data(content) 
        self._log_reading() 
        return processed_content 
    def write(self, content, output_file):
         self._file_reader.write(content, output_file) 
         self._log_writing(output_file)
    def _process_data(self, content): 
         processor = DataProcessor(content) 
         return processor.process_text_without_regex()
    def extract_zip(self,zip_file_path, extract_to):
         with zipfile.ZipFile(zip_file_path, 'r') as zip_ref: 
             zip_ref.extractall(extract_to)
             extracted_files = zip_ref.namelist() 
         return os.path.join(extract_to, extracted_files[0])
    def _log_reading(self):
        print(f"File {self._file_reader.file_path} was read successfully.")
    def _log_writing(self, output_file): 
        print(f"File {output_file} was written successfully.")
