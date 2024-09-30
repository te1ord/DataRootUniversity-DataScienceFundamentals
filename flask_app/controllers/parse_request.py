from flask import request

# request.from is correct server-side method for application/x-www-form-urlencoded content type
# to_dict transforms data to key-value pairs
def get_request_data():
    """
    Get keys & values from request (Note that this method should parse requests with content type "application/x-www-form-urlencoded")
    """
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()
    return data