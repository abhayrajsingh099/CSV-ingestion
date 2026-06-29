"""
    Model to store background job status
"""
from django.db import models

from django.conf import settings

User = settings.AUTH_USER_MODEL

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')

    file_path = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_path[0:30]}-{self.user}"


STATUS_CHOICES = [
    ('Q', 'Queued'),
    ('R', 'Running'),
    ('F', 'Failed'),
    ('C', 'Completed'),
]

class JobStatus(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='jobstatus')
    celery_id = models.CharField(max_length=255, unique=True, editable=False, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='Q')
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)

    def __str__(self):
        return self.celery_id



