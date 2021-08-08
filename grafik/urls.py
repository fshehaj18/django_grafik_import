from django.urls import path

from grafik.views import upload_file, process_file

urlpatterns = [
    path('',upload_file),
    path('process-file/<str:filename>',process_file)
]