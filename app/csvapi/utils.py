import time

from django.core.files.storage import default_storage


from django.db import transaction
from product.models import Product



def validate_csv_file(csv_file) -> dict:
    info = {'file_path':'', 'errors':''}

    if not csv_file:
        info['errors'] = 'CSV file not Provided.'
        return info
    if not csv_file.name.endswith('.csv'):
        info['errors'] = 'File is not CSV type.'
        return info

    filename = csv_file.name
    file_path = f'{time.strftime("%Y-%m-%d")}/{filename}'
    relative_path = default_storage.save(f'csv_files/{file_path}', csv_file)
    absolute_path = default_storage.path(relative_path)
    info['file_path'] = absolute_path
    return info


def validate_csv_header_with_fields(model_fields, csv_header) -> dict:
    info = {'valid': False, 'errors':[]}

    if len(model_fields) != len(csv_header):
        if len(model_fields) > len(csv_header):
            info['errors'] = ["Missing csv fields / header."]
        else:
            info['errors'] = ["Extra fields / header are provided then required. Please Remove the extra fields."]

        return info

    match = set(model_fields)
    count = 0
    errors = ["Unknown fields provided.."]

    for field in csv_header:
        if field.lower() in match:
            count += 1
            match.discard(field.lower())
        else:
            errors.append(field)


    if count == len(model_fields):
        info['valid'] = True
    else:
        info['errors'] = [f"missing fields:{match}"]

    return info


def is_positive_number(value_str) -> bool:
    try:
        num = float(value_str)
        return num >= 0
    except (ValueError, TypeError):
        return False  # Not a valid number, so not positive

def validate_row(row, csv_header) -> dict:

    info = {'validated_data_for_db':{} ,'errors':[]}

    if len(row)!=len(csv_header):
        info['errors'] = ['Missing a required field']
        return info

    char_fields = set([field.name for field in Product._meta.fields if field.get_internal_type() == 'CharField'])
    int_fields = set([field.name for field in Product._meta.fields if field.get_internal_type() == 'IntegerField'])

    column_errors = []
    valid_row_data = {}
    col_number = 1
    header_index = 0 # index to access item in csv_header

    for col_data in row:
        current_header = csv_header[header_index]

        if current_header in char_fields:
            if not col_data.strip() or is_positive_number(col_data) or len(col_data)>255:
                column_errors.append(f"Column:{col_number}:'{current_header}': Empty Column or an invalid {current_header}")
            else:
                valid_row_data[current_header] = col_data

        elif current_header in int_fields:
            if not is_positive_number(col_data):
                column_errors.append(f"Column:{col_number}:'{current_header}' Negative or Invalid Values not accepted.")
            else:
                valid_row_data[current_header] = int(col_data)

        else: # csv_header[csv_index] is description textfield
            valid_row_data[current_header] = col_data

        col_number += 1
        header_index += 1

    if len(column_errors) > 0:
        info['errors'] = column_errors
    else:
        info['validated_data_for_db'] = valid_row_data

    return info


# Transaction and Idempotency Implemented
def save_valid_rows_in_db(valid_data=dict) -> dict:
    info = {'skipped':0, 'success':False}

    try:
        with transaction.atomic():
            for data in valid_data:
                if Product.objects.filter(external_product_id=data['external_product_id']).exists():
                    info['skipped'] = info['skipped']+1 # skip for now, Idempotency handling
                else:
                    Product.objects.create(**data)
    except Exception as e:
        return info

    info['success'] = True
    return info
