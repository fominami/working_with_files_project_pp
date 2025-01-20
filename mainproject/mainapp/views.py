import subprocess
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from .utils.encryption import encrypt_data, decrypt_data, SIGNATURE
from .utils.file_operations import TextFileReader, JSONFileReader, YAMLFileReader, XMLFileReader, FileReaderDecorator
from .utils.strategy_archive import EncryptStrategy,ZipArchiveStrategy, FileProcessorContext, RarArchiveStrategy
import tempfile
import zipfile
import rarfile
import os

class FileUploadView(View):
    template_name = 'file_upload.html'
    rar_exe_path = r'C:\Program Files\WinRAR\Rar.exe'

    def get(self, request):
        form = FileUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_type = uploaded_file.name.split('.')[-1]
            output_file_name = request.POST.get('output_file', 'output')
            action = request.POST.get('action')
            output_file_path = None
            
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:#создаем временный файл для работы 
                for chunk in uploaded_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name

            try:
                with open(tmp_file_path, 'rb') as f: 
                    file_data = f.read() 
                if file_data.startswith(SIGNATURE): #если файл зашифрован
                    encrypted_data = file_data[len(SIGNATURE):] 
                    decrypted_data = decrypt_data(encrypted_data)
                    with open(tmp_file_path, 'wb') as f: 
                        f.write(decrypted_data) 
                    print(f"Файл {tmp_file_path} расшифрован.")
                reader = FileReaderDecorator(None) 
                reader.set_file_path(tmp_file_path)
                if zipfile.is_zipfile(tmp_file_path): #если файл архивирован zip
                     extract_to = tempfile.mkdtemp() #временная директория
                     extracted_file_path = reader.extract_zip(tmp_file_path, extract_to) 
                     file_type = extracted_file_path.split('.')[-1] 
                     tmp_file_path = extracted_file_path 
                elif rarfile.is_rarfile(tmp_file_path): #если файл архивирован rar
                    rarfile.UNRAR_TOOL = r'C:\Program Files\WinRAR\UnRAR.exe'
                    extract_to = tempfile.mkdtemp() 
                    extracted_file_path = reader.extract_rar(tmp_file_path, extract_to) 
                    file_type = extracted_file_path.split('.')[-1] 
                    tmp_file_path =extracted_file_path
                if file_type == 'txt': 
                    reader = TextFileReader(tmp_file_path) 
                elif file_type == 'json': 
                    reader = JSONFileReader(tmp_file_path) 
                elif file_type == 'yaml': 
                    reader = YAMLFileReader(tmp_file_path) 
                elif file_type == 'xml': 
                    reader = XMLFileReader(tmp_file_path) 
                else: 
                    return HttpResponse("Unsupported file type.", status=400)
                       

                   
                decorated_reader = FileReaderDecorator(reader)
                content = decorated_reader.read()
                
                output_file_path = os.path.join(tempfile.gettempdir(), f"{output_file_name}.{file_type}") #путь к временному файлу и запись в него результатов
                decorated_reader.write(content, output_file_path) 
                new_output_file_path = os.path.join(tempfile.gettempdir(), f"{output_file_name}.{file_type}") 

                context = FileProcessorContext(None) 
                if action == "encrypt": 
                    strategy = EncryptStrategy() 
                elif action == "archive": 
                    strategy = ZipArchiveStrategy() 
                    new_output_file_path = os.path.join(tempfile.gettempdir(), f"{output_file_name}.zip") 
                elif action == "rararchive": 
                    rar_exe_path = r'C:\Program Files\WinRAR\Rar.exe'
                    strategy = RarArchiveStrategy(rar_exe_path) 
                    new_output_file_path = os.path.join(tempfile.gettempdir(), f"{output_file_name}.rar") 
                else: strategy = None 
                
                if strategy: 
                    context.set_strategy(strategy) 
                    context.execute_strategy(output_file_path, new_output_file_path)
               
                with open(new_output_file_path, 'rb') as f: 
                    response = HttpResponse(f.read(), content_type='application/octet-stream') #содержимое файла в виде потокового файла для скачивания 
                    if action=="archive":
                        filename = f"{output_file_name}.zip" 
                    elif action=="rararchive":
                        filename = f"{output_file_name}.rar" 
                    else:
                        filename =f"{output_file_name}.{file_type}"
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'#именно закгрузка, а не показ в браузере
                    return response

            finally: #очищение ресурсов
                os.remove(tmp_file_path)
                if output_file_path and os.path.exists(output_file_path): 
                    os.remove(output_file_path)

        return render(request, self.template_name, {'form': form})
