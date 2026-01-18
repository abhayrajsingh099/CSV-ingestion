"""
Csv api logic to accept csv from client-side.
"""

from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

import csv
from io import StringIO

from product.models import Product

from .utils import validate_csv_header_with_fields


@api_view(['POST'])
def upload_csv_file(request):
    # parser_classes = [FileUploadParser]

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
    csv_header = next(csv_reader, None)

    # match fields required model_fields==csv_fields.
    flag = validate_csv_header_with_fields(model_fields, csv_header)
    if type(flag)==list:
        return Response({'errors':flag}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message':'csv file uploaded', 'csv_status':'accepted'},status=status.HTTP_200_OK)
