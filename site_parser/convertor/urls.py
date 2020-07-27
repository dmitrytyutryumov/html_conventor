from django.urls import path
from .views import ConvertorView

urlpatterns = [
    path('html/', ConvertorView.as_view(), name='convert_html_to_pdf'),
]
