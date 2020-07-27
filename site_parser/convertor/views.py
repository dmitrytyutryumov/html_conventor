# Create your views here.
from django.http import FileResponse
from rest_framework import status
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import ConvertorRequestSerializer
from .tasks import convert_html_to_pdf
from .models import ConvertorData


class ConvertorView(views.APIView):
    serializer_class = ConvertorRequestSerializer
    model = ConvertorData
    """
    API endpoint that convert html to pdf.
    """

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            entity = self.model(**serializer.validated_data)
            entity.save()
            convert_html_to_pdf.apply_async(kwargs={'pk': entity.pk})
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
