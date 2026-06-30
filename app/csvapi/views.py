"""
Csv api logic to accept csv from client-side.
"""
import uuid
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .tasks import csv_data
from .models import JobStatus
from .serializers import JobSerializer, DocumentSerializer
from .utils import validate_csv_file
from .models import Document



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv_file(request):

    csv_file = request.FILES.get('file')

    #file validation
    file = validate_csv_file(csv_file)
    if not file['file_path']:
        return Response({'errors':file['errors']}, status=status.HTTP_400_BAD_REQUEST)

    #job created,
    #FIX:- no need for task_id instead when job is created use that id
    task_id = uuid.uuid4()
    try:
        document = Document.objects.create(
            user=request.user,
            file_path=file['file_path']
        )
        JobStatus.objects.create(
            celery_id=task_id,
            document=document
        )
    except Exception as e:
        return Response({'errors':f"Job creation failed. Try again {e}"}, status=status.HTTP_400_BAD_REQUEST)

    #background job
    csv_data.apply_async(args=[file['file_path']], task_id=task_id)

    context = {'csv_status':'accepted',
               'job_status':'is being processed u will be notified.',
               'job_id':task_id}
    return Response(context ,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_job_status(request, id):

    job = (
        JobStatus.objects
        .select_related("document")
        .get(celery_id=id, document__user=request.user)
    )
    serializer = JobSerializer(job)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def documents(request):
    document_lists = Document.objects.filter(user=request.user)

    serializer = DocumentSerializer(document_lists, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)








