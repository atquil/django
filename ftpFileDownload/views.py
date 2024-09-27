from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from rest_framework import status
from django.db import connections
from .serializers import  MultipleClientFileDownloadSerializer
import ftplib
from datetime import datetime, timedelta
import logging
from rest_framework.response import Response

from django.shortcuts import render

logger = logging.getLogger(__name__)



# To map frontEnd
def index(request):
    return render(request, 'index.html')


# Download Single File 
# class FTPDownloadView(APIView):
#     def get(self, request, format=None):
#         serializer = FtpFileDownload(data=request.query_params)

#         if serializer.is_valid():
#             clientName = serializer.validated_data['clientName']

#             # FTP Related Data
#             fileName = serializer.validated_data['fileName']
#             ftp_directory = f'/path/to/files/{clientName}/'
#             ftp_server = 'ftp.example.com'
#             ftp_user = 'your_username'
#             ftp_password = 'your_password'

#             try:
#                 ftp = ftplib.FTP(ftp_server)
#                 ftp.login(user=ftp_user, passwd=ftp_password)
#                 ftp.cwd(ftp_directory)



#                 files = ftp.nlst()

#                 matching_files = [f for f in files if f.startswith(fileName)]
#                 if not matching_files:
#                     return HttpResponse("File not found", status=404)

#                 file_to_download = matching_files[0]
#                 response = HttpResponse(content_type='application/octet-stream')
#                 response['Content-Disposition'] = f'attachment; filename="{file_to_download}"'

#                 ftp.retrbinary(f"RETR {file_to_download}", response.write)
#                 ftp.quit()
#                 return response
#             except ftplib.all_errors as e:
#                 return HttpResponse(f"FTP error: {str(e)}", status=500)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def get_ticker_client_map(ticker_names):
    try:
        logger.info("Successfully fetched ticker-client map.")
        # Create a string of placeholders for the query
        placeholders = ', '.join(['%s'] * len(ticker_names))
        query = f"""
            SELECT indexTicker, ClientName
            FROM your_table_name
            WHERE indexTicker IN ({placeholders})
        """

        with connections['ftpDownload'].cursor() as cursor:
            cursor.execute(query, ticker_names)
            fetched_data = cursor.fetchall()
            ticker_client_map = {row[0]: row[1] for row in fetched_data}

        # Check for missing ticker names
        missing_tickers = [ticker for ticker in ticker_names if ticker not in ticker_client_map]
        if missing_tickers:
            logger.warning(f"Ticker names not found: {missing_tickers}")

        logger.info("Successfully fetched ticker-client map.")
        return ticker_client_map
    except Exception as e:
        logger.error(f"Error fetching ticker-client map: {str(e)}")
        return None



def generate_file_names(ticker_names, start_date, end_date, file_type, ticker_client_map):
    file_groups = {}
    for ticker_name in ticker_names:
        client_name = ticker_client_map.get(ticker_name)
        if not client_name:
            logger.warning(f"Client name not found for ticker: {ticker_name}")
            continue

        file_names = []
        current_date = start_date
        while current_date <= end_date:
            file_name = f"{file_type}-{ticker_name}-{current_date.strftime('%Y-%m-%d')}"
            file_names.append(file_name)
            current_date += timedelta(days=1)

        if client_name not in file_groups:
            file_groups[client_name] = []
        file_groups[client_name].extend(file_names)
    logger.info("Successfully generated file names.")
    return file_groups

class FTPMultipleFileDownloadView(APIView):
    def post(self, request, format=None):
        serializer = MultipleClientFileDownloadSerializer(data=request.data)

        if serializer.is_valid():
            ticker_names = serializer.validated_data['tickerNames']
            date_range = serializer.validated_data['dateRange']
            file_type = serializer.validated_data['fileType']

            start_date, end_date = date_range.split(' to ')
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            ftp_server = 'ftp.example.com'
            ftp_user = 'your_username'
            ftp_password = 'your_password'

            ticker_client_map = get_ticker_client_map(ticker_names)
            if ticker_client_map is None:
                return JsonResponse({'error': 'Error fetching ticker-client map'}, status=500)

            file_groups = generate_file_names(ticker_names, start_date, end_date, file_type, ticker_client_map)
            logger.info("----------File Data-----------")
            for file in file_groups:
                logger.info("File Data"+file)
            
            return self.download_files_from_ftp(file_groups, ftp_server, ftp_user, ftp_password)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import os
def download_files_from_ftp(file_groups, ftp_server, ftp_user, ftp_password, download_dir='downloads'):
    results = {
        'success': [],
        'failure': []
    }
    try:
        ftp = ftplib.FTP(ftp_server)
        ftp.login(user=ftp_user, passwd=ftp_password)
        logger.info("Successfully connected to FTP server.")

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            logger.info(f"Created download directory: {download_dir}")

        for client_name, file_names in file_groups.items():
            ftp_directory = f'/path/to/files/{client_name}/'
            try:
                ftp.cwd(ftp_directory)
                files = ftp.nlst()
                for file_name in file_names:
                    matching_files = [f for f in files if f.startswith(file_name)]
                    if not matching_files:
                        results['failure'].append({'clientName': client_name, 'fileName': file_name, 'status': 'File not found'})
                        logger.warning(f"File not found: {file_name}")
                        continue

                    for file_to_download in matching_files:
                        local_filename = os.path.join(download_dir, f"{client_name}_{file_to_download}")
                        with open(local_filename, 'wb') as local_file:
                            ftp.retrbinary(f"RETR {file_to_download}", local_file.write)
                        results['success'].append({'clientName': client_name, 'fileName': file_to_download, 'status': 'Success'})
                        logger.info(f"Successfully downloaded file: {file_to_download} to {local_filename}")
            except ftplib.all_errors as e:
                results['failure'].append({'clientName': client_name, 'fileName': file_name, 'status': f'FTP error: {str(e)}'})
                logger.error(f"FTP error for client {client_name}: {str(e)}")

        ftp.quit()
        logger.info("FTP session closed.")
    except ftplib.all_errors as e:
        logger.error(f"FTP connection error: {str(e)}")
        return {'error': f'FTP error: {str(e)}'}, 500
    return results, 200


class FTPMultipleFileDownloadView(APIView):
    def post(self, request, format=None):
        serializer = MultipleClientFileDownloadSerializer(data=request.data)

        if serializer.is_valid():
            ticker_names = serializer.validated_data['tickerNames']
            date_range = serializer.validated_data['dateRange']
            file_type = serializer.validated_data['fileType']

            start_date, end_date = date_range.split(' to ')
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            ftp_server = 'ftp.example.com'
            ftp_user = 'your_username'
            ftp_password = 'your_password'

            ticker_client_map = get_ticker_client_map(ticker_names)
            if ticker_client_map is None:
                return JsonResponse({'error': 'Error fetching ticker-client map'}, status=500)

            file_groups = generate_file_names(ticker_names, start_date, end_date, file_type, ticker_client_map)
            logger.info("----------File Data-----------")
            for file in file_groups:
                logger.info("File Data"+file)
            
            results, status_code = download_files_from_ftp(file_groups, ftp_server, ftp_user, ftp_password)

            return JsonResponse(results, safe=False, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




        