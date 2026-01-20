from product.models import Product


def validate_csv_header_with_fields(model_fields, csv_header):
    if len(model_fields) != len(csv_header):
        if len(model_fields) > len(csv_header):
            return ["Missing csv fields/header."]
        else:
            return ["Extra fields/header are provided then required."]

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
        return True
    else:
        errors.append(f"missing fields:{match}")

    return errors



def is_positive_number(value_str):
    try:
        num = float(value_str)
        return num >= 0
    except (ValueError, TypeError):
        return False  # Not a valid number, so not positive

def validate_row(row, csv_header):
    if len(row)!=len(csv_header):
        return ['Missing a required field']
    char_fields = set([field.name for field in Product._meta.fields if field.get_internal_type() == 'CharField'])
    int_fields = set([field.name for field in Product._meta.fields if field.get_internal_type() == 'IntegerField'])

    column_errors = []
    row_data_for_db = {}
    col_number = 1
    csv_index = 0 # index to access item in csv_header

    for col_data in row:
        current_header = csv_header[csv_index]

        if current_header in char_fields:
            if not col_data.strip() or is_positive_number(col_data) or len(col_data)>255:
                column_errors.append(f"Column:{col_number}:'{csv_header[csv_index]}': Empty Column or an invalid {current_header}")
            else: #add to db data for use
                row_data_for_db[current_header] = col_data

        elif current_header in int_fields:
            if not is_positive_number(col_data):
                column_errors.append(f"Column:{col_number}:'{current_header}' Negative or Invalid Values not accepted.")
            else: #add to db data for use
                row_data_for_db[current_header] = int(col_data)

        else: # csv_header[csv_index] is description textfield
            row_data_for_db[current_header] = col_data

        col_number += 1
        csv_index += 1

    #errors inside the row return not save
    if len(column_errors) > 0:
        return column_errors

    return row_data_for_db







