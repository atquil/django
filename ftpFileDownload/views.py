from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connections, OperationalError
# Import file from .serializers file 
from .serializers import ClientInfoSerializer, FtpFileDownload


# Api Routing on what it will do 

# class GetClientInfoUsingTickerNameAndDate(APIView):

#     # Get API
#     def get(self, request, format=None):
#         # Extracting the query parameter
#         serializer = ClientInfoSerializer(data=request.query_params)

#         # Validating If the parameters are correct
#         if serializer.is_valid():
            
            
#             data = {
#                 "clientName": "John Doe",
#                 "tickerName": serializer.validated_data['ticker'],
#                 "datesCreated": serializer.validated_data['date'].strftime('%Y-%m-%d')
#             }
#             return Response(data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetClientInfoUsingTickerNameAndDate(APIView):

    def get(self, request, format=None):
        serializer = ClientInfoSerializer(data=request.query_params)

        if serializer.is_valid():
            date = serializer.validated_data['date'].strftime('%Y-%m-%d')
            ticker_name = serializer.validated_data['ticker']

            try:
                with connections['external_db'].cursor() as cursor:
                    cursor.execute("""
                        SELECT client_name, ticker_name, date
                        FROM your_table_name
                        WHERE date = %s AND ticker_name = %s
                    """, [date, ticker_name])
                    
                    rows = cursor.fetchall()

                if rows:
                    data = [
                        {'clientName': row[0], 'tickerName': row[1], 'datesCreated': row[2].strftime('%Y-%m-%d')}
                        for row in rows
                    ]
                else:
                    data = {
                        "clientName": "John Doe",
                        "tickerName": ticker_name,
                        "datesCreated": date
                    }
                return Response(data, status=status.HTTP_200_OK)
            except OperationalError as e:
                data = {
                    "clientName": "John Doe",
                    "tickerName": ticker_name,
                    "datesCreated": date
                }
                return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# To add frontend url
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')



# For downloading FTP Files 

import ftplib
from django.http import HttpResponse

class FTPDownloadView(APIView):
    def get(self, request, format=None):
        serializer = FtpFileDownload(data=request.query_params)

        if serializer.is_valid():
            clientName = serializer.validated_data['clientName']

            # FTP Related Data
            fileName = serializer.validated_data['fileName']
            ftp_directory = f'/path/to/files/{clientName}/'
            ftp_server = 'ftp.example.com'
            ftp_user = 'your_username'
            ftp_password = 'your_password'

            try:
                ftp = ftplib.FTP(ftp_server)
                ftp.login(user=ftp_user, passwd=ftp_password)
                ftp.cwd(ftp_directory)
                files = ftp.nlst()

                matching_files = [f for f in files if f.startswith(fileName)]
                if not matching_files:
                    return HttpResponse("File not found", status=404)

                file_to_download = matching_files[0]
                response = HttpResponse(content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{file_to_download}"'

                ftp.retrbinary(f"RETR {file_to_download}", response.write)
                ftp.quit()
                return response
            except ftplib.all_errors as e:
                return HttpResponse(f"FTP error: {str(e)}", status=500)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)