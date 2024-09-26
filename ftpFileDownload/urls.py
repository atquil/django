from django.urls import path

# Import the API that has been created, and configure the URLs
from .views import FTPMultipleFileDownloadView,index

urlpatterns = [
    path('', index, name='index'),
    path('multiple-client-file-download/', FTPMultipleFileDownloadView.as_view(), name='ftp-multiple-file-download'),
]