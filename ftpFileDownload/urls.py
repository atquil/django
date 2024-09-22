from django.urls import path

# Import the API that has been created, and configure the URLs
from .views import GetClientInfoUsingTickerNameAndDate

urlpatterns = [
    path('get-client-data/', GetClientInfoUsingTickerNameAndDate.as_view(), name='get-client-data'),
]