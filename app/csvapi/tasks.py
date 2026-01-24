from celery import shared_task , current_task
import csv
import random
from django.utils import timezone

from product.models import Product
from .models import JobStatus
from .utils import (validate_csv_header_with_fields,
                    validate_row, save_valid_rows_in_db)

@shared_task(
        bind=True,
        autoretry_for=(Exception,),
        max_retries=3,
        retry_backoff=True
)
def csv_data(self, file_path): # celery -A core worker -l info --pool=solo
    task_id = current_task.request.id
    job_instance = JobStatus.objects.get(celery_id=task_id)

    # Celery Retry Logic
    if job_instance.status in ['C', 'F']: # No retry
        return f"No Need to Retry Task. Job status:{job_instance.status}"
    elif job_instance.status in ['R']: #retry available
        job_instance.retry_count = self.request.retries
        if job_instance.retry_count >= self.max_retries:
            job_instance.status = 'F'
            job_instance.finished_at = timezone.now()
            job_instance.summary = {'error':[job_instance.summary],
                                    'Celery_info':{'retries_used':job_instance.retry_count,
                                                   'retries_left':self.max_retries-job_instance.retry_count,
                                                   'retrying':'No'},
                                    }
            job_instance.save()
            return f"Max retries achieved transfered job to terminal.{job_instance.retry_count}"
    else: #first execution
        job_instance.status = 'R'
        job_instance.save()

    #models fields
    model_fields = [field.name for field in Product._meta.fields if not field.name=='id']
    # using csv module
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        csv_header = next(csv_reader)

        # header validation
        header_info = validate_csv_header_with_fields(model_fields, csv_header)
        if not header_info['valid']:
            job_instance.status = 'F'
            job_instance.summary = {'errors':header_info['errors'], 'Celery_info':{'retry_status':"No retry validaion failed."}}
            job_instance.finished_at = timezone.now()
            job_instance.save()
            return

        #Row validation and collecting valid rows
        row_number = 2
        row_errors = {}
        valid_rows_data = []
        valid_rows_count = 0

        for row in csv_reader:
            row_info = validate_row(row, csv_header)

            if row_info['validated_data_for_db']:
                valid_rows_data.append(row_info['validated_data_for_db'])
                valid_rows_count += 1
            else:
                row_errors['Row:'+str(row_number)] = row_info['errors']

            row_number += 1


    #send valid data/rows to transicational.atomic function
    db_status = save_valid_rows_in_db(valid_rows_data)
    if not db_status['success']:
        job_instance.summary = 'Unexcpeted Error during save. Trying again.'
        job_instance.save()
        raise Exception()


    #return valid response
    context = {'Csv_information':{'Total rows':row_number-2,
                   'Rows Accepted':valid_rows_count,
                   'Rows Rejected':row_number-valid_rows_count-2,
                   'Rows Created (New data)': valid_rows_count-db_status['skipped'],
                   'Rows Skipped (Already existed data)': db_status['skipped'],
                   'row_errors':row_errors},
            'Celery_info':{'retry_used':job_instance.retry_count,
                            'retries_left':self.max_retries-job_instance.retry_count,
                            'retrying':'No'},
                   }

    job_instance.status = 'C'
    job_instance.summary = context
    job_instance.finished_at = timezone.now()
    job_instance.save()

    return 'Success'