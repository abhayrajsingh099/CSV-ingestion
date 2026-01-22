"""
Csv api logic to accept csv from client-side.
"""
import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .tasks import csv_data
from .models import JobStatus
from .serializers import JobSerializer
from .utils import validate_csv_file

@api_view(['POST'])
def upload_csv_file(request):

    csv_file = request.FILES.get('file')

    #file validation
    file = validate_csv_file(csv_file)
    if not file['file_path']:
        return Response({'errors':file['errors']}, status=status.HTTP_400_BAD_REQUEST)

    #job created
    task_id = uuid.uuid4()
    try:
        JobStatus.objects.create(celery_id=task_id)
    except Exception as e:
        return Response({'errors':"Job creation failed. Try again"}, status=status.HTTP_400_BAD_REQUEST)

    #background job
    csv_data.apply_async(args=[file['file_path']], task_id=task_id)

    context = {'csv_status':'accepted',
               'job_status':'is being processed u will be notified.',
               'job_id':task_id}
    return Response(context ,status=status.HTTP_200_OK)


@api_view(['POST'])
def check_job_status(request, id):

    job = get_object_or_404(JobStatus, celery_id=id)
    serializer = JobSerializer(job)

    return Response(serializer.data, status=status.HTTP_200_OK)



