"""
Csv api logic to accept csv from client-side.
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import csv
from io import StringIO

from product.models import Product

from .utils import validate_csv_header_with_fields, validate_row


@api_view(['POST'])
def upload_csv_file(request):

    csv_file = request.FILES.get('file')

    # file accepted or not
    if not csv_file:
        return Response({'errors':'CSV file not Provided.'}, status=status.HTTP_400_BAD_REQUEST)
    if not csv_file.name.endswith('.csv'): #python method
        return Response({'errors':'File is not CSV type.'}, status=status.HTTP_400_BAD_REQUEST)

    # make csv content available in buffer
    content = csv_file.read().decode('utf-8')
    string_io = StringIO(content)

    #models fields
    model_fields = [field.name for field in Product._meta.fields if not field.name=='id']
    #using csv module
    csv_reader = csv.reader(string_io)
    csv_header = next(csv_reader, None) #header of csv

    # match fields required model_fields==csv_fields.
    flag = validate_csv_header_with_fields(model_fields, csv_header)
    if type(flag)==list:
        return Response({'errors':flag}, status=status.HTTP_400_BAD_REQUEST)

    #iterate rows
    row_number = 2
    row_errors = {}
    valid_rows_count = 0

    for row in csv_reader:
        validated = validate_row(row, csv_header)
        if type(validated)==list:
            row_errors['Row:'+str(row_number)] = validated
        else: # if no errors row is safe save row into DB
            try:
                Product.objects.create(**validated)
                valid_rows_count += 1
            except Exception as e:
                row_errors['Row:'+str(row_number)] = f'Unexpected Error during Save. {e}'

        row_number += 1

    if len(row_errors) > 0:
        context = {'Total rows':str(row_number-2),
                   'Rows Accepted':str(valid_rows_count),
                   'Rows Rejected':str(row_number-valid_rows_count-2),
                   'row_erros':row_errors
                   }
        return Response(context, status=status.HTTP_207_MULTI_STATUS)


    context = {'csv_status':'accepted', 'Rows Accepted':str(valid_rows_count)}
    return Response(context ,status=status.HTTP_200_OK)
