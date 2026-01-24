from celery import shared_task ,  current_task
import csv
from django.utils import timezone

from product.models import Product
from .models import JobStatus
from .utils import (validate_csv_header_with_fields,
                    validate_row, save_valid_rows_in_db)

@shared_task
def csv_data(file_path): # celery -A core worker -l info --pool=solo
    task_id = current_task.request.id
    job_instance = JobStatus.objects.get(celery_id=task_id)

    # Making retry safe, if job in terminal state, reject retry
    if job_instance.status in ['C', 'F']:
        return f"No Need to Retry Task. Job status:{job_instance.status}"
    else:
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
            job_instance.summary = header_info['errors']
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
        return


    #return valid response
    context = {'Total rows':row_number-2,
                   'Rows Accepted':valid_rows_count,
                   'Rows Rejected':row_number-valid_rows_count-2,
                   'Rows Created (New data)': valid_rows_count-db_status['skipped'],
                   'Rows Skipped (Already existed data)': db_status['skipped'],
                   'row_errors':row_errors
                   }

    job_instance.status = 'C'
    job_instance.summary = context
    job_instance.finished_at = timezone.now()
    job_instance.save()

    return 'Success'