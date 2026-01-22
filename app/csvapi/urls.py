from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.upload_csv_file, name='upload_csv'),
    path('status/<str:id>', views.check_job_status, name='job_status'),
]