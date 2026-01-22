
from rest_framework import serializers

from .models import JobStatus

class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobStatus
        fields =  '__all__' #['celery_id' ,'status.get_status_display()', 'summary']