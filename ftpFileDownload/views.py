from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Import file from .serializers file 
from .serializers import ClientInfoSerializer


# Api Routing on what it will do 
class GetClientInfoUsingTickerNameAndDate(APIView):

    # Get API
    def get(self, request, format=None):
        # Extracting the query parameter
        serializer = ClientInfoSerializer(data=request.query_params)

        # Validating If the parameters are correct
        if serializer.is_valid():

            
            data = {
                "clientName": "John Doe",
                "tickerName": serializer.validated_data['ticker'],
                "datesCreated": serializer.validated_data['date'].strftime('%Y-%m-%d')
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# To add frontend url
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')