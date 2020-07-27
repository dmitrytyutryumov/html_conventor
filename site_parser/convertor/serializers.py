from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers


class SourceField(serializers.Field):
    def __init__(self, *args, **kwargs):
        super(SourceField, self).__init__(*args, **kwargs)
        self.file_serializer = serializers.FileField(**kwargs)
        self.url_serializer = serializers.URLField(**kwargs)

    def to_internal_value(self, data):
        if isinstance(data, str):
            return self.url_serializer.to_internal_value(data)
        if isinstance(data, InMemoryUploadedFile):
            value = self.file_serializer.to_internal_value(data)
            return value.open().read().decode()


class ConvertorRequestSerializer(serializers.Serializer):
    source = SourceField(required=True)
    email = serializers.EmailField(required=False)
    domain = serializers.URLField(required=False)

