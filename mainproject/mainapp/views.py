

import subprocess
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from .utils.file_operations import TextFileReader, JSONFileReader, YAMLFileReader, XMLFileReader, FileReaderDecorator

import tempfile
import zipfile
import rarfile
import os

class FileUploadView(View):
    template_name = 'file_upload.html'

    def get(self, request):
        form = FileUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_type = uploaded_file.name.split('.')[-1]
            output_file_name = request.POST.get('output_file', 'output')
            archive = request.POST.get('archive')
            rararchive = request.POST.get('rararchive')
            output_file_path = None
            
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in uploaded_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name

            try:
                reader = FileReaderDecorator(None) 
                reader.set_file_path(tmp_file_path)
                if zipfile.is_zipfile(tmp_file_path): 
                     extract_to = tempfile.mkdtemp() 
                     extracted_file_path = reader.extract_zip(tmp_file_path, extract_to) 
                     file_type = extracted_file_path.split('.')[-1] 
                     tmp_file_path = extracted_file_path 
                elif rarfile.is_rarfile(tmp_file_path): 
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
                
                output_file_path = os.path.join(tempfile.gettempdir(), f"{output_file_name}.{file_type}")
                decorated_reader.write(content, output_file_path) 
                if archive: 
                    output_file_path = os.path.join(tempfile.gettempdir(), f"{output_file_name}.{file_type}")
                    zip_output_file_path = os.path.join(tempfile.gettempdir(), f"{output_file_name}.zip") 
                    with zipfile.ZipFile(zip_output_file_path, 'w') as zipf: 
                        zipf.write(output_file_path, arcname=f"{output_file_name}.{file_type}") 
                    output_file_path = zip_output_file_path
                if rararchive: 
                    rar_exe_path = r'"C:\Program Files\WinRAR\Rar.exe"' 
                    rar_output_file_path = os.path.join(tempfile.gettempdir(), f"{output_file_name}.rar") 
                    if not os.path.isfile(output_file_path): 
                        raise FileNotFoundError(f"The file {output_file_path} does not exist.")
                    subprocess.run([rar_exe_path, 'a', rar_output_file_path, output_file_path], check=True, capture_output=True, text=True)
                    output_file_path =rar_output_file_path
                with open(output_file_path, 'rb') as f: 
                    response = HttpResponse(f.read(), content_type='application/octet-stream') 
                    filename = f"{output_file_name}.zip" if archive else f"{output_file_name}.{file_type}"
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                    return response

            finally:
                os.remove(tmp_file_path)
                if output_file_path and os.path.exists(output_file_path): 
                    os.remove(output_file_path)

        return render(request, self.template_name, {'form': form})
