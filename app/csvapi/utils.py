

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


