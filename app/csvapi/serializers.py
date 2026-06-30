
from rest_framework import serializers

from .models import JobStatus, Document

class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobStatus
        fields =  '__all__' #['celery_id' ,'status.get_status_display()', 'summary']

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'