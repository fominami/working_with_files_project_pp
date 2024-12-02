from django.urls import path
from . import views

urlpatterns = [
    path(' ', views.FileUploadView.as_view(), name='file_upload'),
]
