from abc import ABC, abstractmethod
import zipfile
import os
import subprocess
from .encryption import encrypt_data, SIGNATURE

class Strategy(ABC):
    @abstractmethod
    def execute(self, input_file_path, output_file_path):
        pass

class ZipArchiveStrategy(Strategy):
    def execute(self, input_file_path, output_file_path):
        with zipfile.ZipFile(output_file_path, 'w') as zipf:
            zipf.write(input_file_path, arcname=os.path.basename(input_file_path))

class RarArchiveStrategy(Strategy):
    def __init__(self, rar_exe_path):
        self.rar_exe_path = rar_exe_path

    def execute(self, input_file_path, output_file_path):
        

        result = subprocess.run([self.rar_exe_path, 'a', output_file_path, input_file_path], check=True, capture_output=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to create RAR archive: {result.stderr.decode()}")


class EncryptStrategy(Strategy):
    def execute(self, input_file_path, output_file_path):
        with open(input_file_path, 'rb') as f:
            file_data = f.read()
        encrypted_data = SIGNATURE + encrypt_data(file_data)
        with open(output_file_path, 'wb') as f:
            f.write(encrypted_data)
class FileProcessorContext:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy

    def execute_strategy(self, input_file_path, output_file_path):
        self._strategy.execute(input_file_path, output_file_path)
