"""
Csv api logic to accept csv from client-side.
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import csv
from io import StringIO

from product.models import Product

from .utils import (validate_csv_header_with_fields,
                    validate_row, save_valid_rows_in_db)


@api_view(['POST'])
def upload_csv_file(request):

    csv_file = request.FILES.get('file')

    # file accepted or not
    if not csv_file:
        return Response({'errors':'CSV file not Provided.'}, status=status.HTTP_400_BAD_REQUEST)
    if not csv_file.name.endswith('.csv'): #python method
        return Response({'errors':'File is not CSV type.'}, status=status.HTTP_400_BAD_REQUEST)

    # make csv content available in buffer (in-memory usage of csv)
    content = csv_file.read().decode('utf-8')
    string_io = StringIO(content)
    #models fields
    model_fields = [field.name for field in Product._meta.fields if not field.name=='id']
    #using csv module
    csv_reader = csv.reader(string_io)
    csv_header = next(csv_reader, None)

    # header validation
    header_info = validate_csv_header_with_fields(model_fields, csv_header)
    if not header_info['valid']:
        return Response({'errors':header_info['errors']}, status=status.HTTP_400_BAD_REQUEST)

    #Row validation and saving data into db
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
    if not db_status:
        return Response({'errors':'Unexcpeted Error during save. Try again.'}, status=status.HTTP_400_BAD_REQUEST)


    #return valid response
    if len(row_errors) > 0:
        context = {'Total rows':str(row_number-2),
                   'Rows Accepted':str(valid_rows_count),
                   'Rows Rejected':str(row_number-valid_rows_count-2),
                   'row_errors':row_errors
                   }
        return Response(context, status=status.HTTP_207_MULTI_STATUS)


    context = {'csv_status':'accepted', 'Rows Accepted':str(valid_rows_count)}
    return Response(context ,status=status.HTTP_200_OK)
