from rest_framework import serializers

class ClientInfoSerializer(serializers.Serializer):
    # Validations are also added for the format
    date = serializers.DateField(format='%y%m%d', input_formats=['%y%m%d'])
    ticker = serializers.CharField(max_length=10)

