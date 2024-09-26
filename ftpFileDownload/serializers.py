from rest_framework import serializers


#For Single File download
# class FtpFileDownload(serializers.Serializer):
#     # Validations are also added for the format
#     fileName = serializers.CharField()
#     clientName = serializers.CharField()


#For multiple files download
class MultipleClientFileDownloadSerializer(serializers.Serializer):
    tickerNames = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )
    dateRange = serializers.CharField(max_length=100)
    fileType = serializers.CharField(max_length=10)

    