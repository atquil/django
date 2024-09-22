from django.urls import path

# Import the API that has been created, and configure the URLs
from .views import FTPDownloadView, GetClientInfoUsingTickerNameAndDate,index

urlpatterns = [
    path('get-client-data/', GetClientInfoUsingTickerNameAndDate.as_view(), name='get-client-data'),
    path('', index, name='index'),
    path('download/', FTPDownloadView.as_view(), name='ftp-download'),
]