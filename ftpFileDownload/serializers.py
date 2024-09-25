from rest_framework import serializers

class ClientInfoSerializer(serializers.Serializer):
    # Validations are also added for the format
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    ticker = serializers.CharField(max_length=10)

class FtpFileDownload(serializers.Serializer):
    # Validations are also added for the format
    fileName = serializers.CharField()
    clientName = serializers.CharField()

# To take the information of ticker , clientName
class TickerInformation(serializers.Serializer):
    # Validations are also added for the format
    ticker = serializers.CharField()
    clientName = serializers.CharField()

# To have List of Dictionary for clientName and FileName
class FileRequestSerializer(serializers.Serializer):
    clientName = serializers.CharField(max_length=100)
    fileName = serializers.CharField(max_length=100)

class FTPMultipleFileDownloadSerializer(serializers.Serializer):
    fileRequests = serializers.ListField(
        child=FileRequestSerializer()
    )

class MultipleClientFileDownloadSerializer(serializers.Serializer):
    tickerNames = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )
    dateRange = serializers.CharField(max_length=100)
    fileType = serializers.CharField(max_length=10)

    