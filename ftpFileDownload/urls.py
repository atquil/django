from django.urls import path

# Import the API that has been created, and configure the URLs
from .views import FTPDownloadView, FTPMultipleFileDownloadView, GetAllTickerAndClientCombination, GetClientInfoUsingTickerNameAndDate,index

urlpatterns = [
    path('get-client-data/', GetClientInfoUsingTickerNameAndDate.as_view(), name='get-client-data'),
    path('get-ticker-and-client-data/', GetAllTickerAndClientCombination.as_view(), name='get-ticker-and-client-data'),
    path('', index, name='index'),
    path('download/', FTPDownloadView.as_view(), name='ftp-download'),
    path('multiple-client-file-download/', FTPMultipleFileDownloadView.as_view(), name='ftp-multiple-file-download'),
]