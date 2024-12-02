

import json
import yaml
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

class FileReader(ABC):
    @abstractmethod
    def read(self):
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
            # Попробуйте другую кодировку, например 'windows-1251' для русских текстов
            with open(self.file_path, 'r', encoding='windows-1251') as f:
                content = f.read()
        return content



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


class XMLFileReader(FileReader):
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return root

class FileReaderDecorator(FileReader):
    def __init__(self, file_reader):
        self._file_reader = file_reader

    def read(self):
        result = self._file_reader.read()
        self._log_reading()
        return result

    def _log_reading(self):
        print(f"File {self._file_reader.file_path} was read successfully.")
