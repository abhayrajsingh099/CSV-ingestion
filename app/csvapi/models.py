"""
    Model to store background job status
"""
from django.utils import timezone
from django.db import models


STATUS_CHOICES = [
    ('Q', 'Queued'),
    ('R', 'Running'),
    ('F', 'Failed'),
    ('C', 'Completed'),
]
class JobStatus(models.Model):
    celery_id = models.CharField(unique=True, editable=False, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='Q')
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(default=timezone.now())
    summary = models.TextField()
    retry_count = models.IntegerField(default=0)

    def __str__(self):
        return self.celery_id
