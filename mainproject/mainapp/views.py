

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from .utils.file_operations import TextFileReader, JSONFileReader, YAMLFileReader, XMLFileReader, FileReaderDecorator
import tempfile
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

            
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in uploaded_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name

            try:
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
                with open(output_file_path, 'rb') as f: 
                    response = HttpResponse(f.read(), content_type='application/octet-stream') 
                    response['Content-Disposition'] = f'attachment; filename="{output_file_name}.{file_type}"'
                    return response

            finally:
                os.remove(tmp_file_path)
                if os.path.exists(output_file_path): 
                    os.remove(output_file_path)

        return render(request, self.template_name, {'form': form})
