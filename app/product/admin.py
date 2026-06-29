"""
Admin Panel Custom.
"""

from django.contrib import admin

from .models import Product
from csvapi.models import JobStatus, Document


admin.site.register(JobStatus)
admin.site.register(Product)
admin.site.register(Document)

