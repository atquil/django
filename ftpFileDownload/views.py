from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connections, OperationalError
# Import file from .serializers file 
from .serializers import ClientInfoSerializer, FTPMultipleFileDownloadSerializer, FtpFileDownload


# Api Routing on what it will do 

#class GetClientInfoUsingTickerNameAndDate(APIView):

    # Get API
    # def get(self, request, format=None):
    #     # Extracting the query parameter
    #     serializer = ClientInfoSerializer(data=request.query_params)

    #     # Validating If the parameters are correct
    #     if serializer.is_valid():
            
            
    #         data = {
    #             "clientName": "John Doe",
    #             "tickerName": serializer.validated_data['ticker'],
    #             "datesCreated": serializer.validated_data['date'].strftime('%Y-%m-%d')
    #         }
    #         return Response(data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllTickerAndClientCombination(APIView):

    def get(self, request, format=None):

        # Dummy data for testing
        dummy_data = [
            {'clientName': 'ClientA', 'tickerName': 'TickerA'},
            {'clientName': 'ClientB', 'tickerName': 'TickerB'},
            {'clientName': 'ClientC', 'tickerName': 'TickerC'},
        ]
        return Response(dummy_data, status=status.HTTP_200_OK)
        # Get all the clientName
        try:
            with connections['ftpDownload..'].cursor() as cursor:
                cursor.execute("""
                    SELECT ClientName, indexTicker
                    FROM your_table_name
                """)
                
                rows = cursor.fetchall()

            if rows:
                data = [
                    {'clientName': row[0], 'tickerName': row[1]}
                    for row in rows
                ]
            else:
                data = []
            return Response(data, status=status.HTTP_200_OK)
        except OperationalError as e:
            return Response({
                "error": "Database connection error",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class GetClientInfoUsingTickerNameAndDate(APIView):

    def get(self, request, format=None):
        serializer = ClientInfoSerializer(data=request.query_params)

        if serializer.is_valid():
            date = serializer.validated_data['date'].strftime('%Y-%m-%d')
            ticker_name = serializer.validated_data['ticker']

            try:
                with connections['ftpDownload..'].cursor() as cursor:
                    cursor.execute("""
                        SELECT ClientName, indexTicker
                        FROM your_table_name
                        WHERE indexTicker = %s
                    """, [ticker_name])
                    
                    rows = cursor.fetchall()

                if rows:
                    data = [
                        {'clientName': row[0], 'tickerName': row[1], 'datesCreated': date}
                        for row in rows
                    ]
                else:
                    data = []
                return Response(data, status=status.HTTP_200_OK)
            except OperationalError as e:
                return Response({
                    "error": "Database connection error",
                    "details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# To add frontend url
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')



# For downloading FTP Files 

import ftplib
from django.http import HttpResponse, JsonResponse

#Download Multiple file based on client and fileName { {clientName:"abc", "fileName":"abc"}}

class FTPMultipleFileDownloadView(APIView):
    def get(self, request, format=None):
        serializer = FTPMultipleFileDownloadSerializer(data=request.query_params)

        if serializer.is_valid():
            file_requests = serializer.validated_data['fileRequests']  # Expecting a list of dictionaries
            ftp_server = 'ftp.example.com'
            ftp_user = 'your_username'
            ftp_password = 'your_password'

            results = []

            try:
                ftp = ftplib.FTP(ftp_server)
                ftp.login(user=ftp_user, passwd=ftp_password)

                for file_request in file_requests:

                    clientName = file_request['clientName']
                    fileName = file_request['fileName']
                    ftp_directory = f'/path/to/files/{clientName}/'

                    try:
                        ftp.cwd(ftp_directory)
                        files = ftp.nlst()
                        matching_files = [f for f in files if f.startswith(fileName)]
                        if not matching_files:
                            results.append({'clientName': clientName, 'fileName': fileName, 'status': 'File not found'})
                            continue

                        file_to_download = matching_files[0]
                        response = HttpResponse(content_type='application/octet-stream')
                        response['Content-Disposition'] = f'attachment; filename="{file_to_download}"'

                        ftp.retrbinary(f"RETR {file_to_download}", response.write)
                        results.append({'clientName': clientName, 'fileName': fileName, 'status': 'Success'})
                    except ftplib.all_errors as e:
                        results.append({'clientName': clientName, 'fileName': fileName, 'status': f'FTP error: {str(e)}'})

                ftp.quit()
                return JsonResponse(results, safe=False)
            except ftplib.all_errors as e:
                return JsonResponse({'error': f'FTP error: {str(e)}'}, status=500)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Download Single File 
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