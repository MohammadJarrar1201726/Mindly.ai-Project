from flask import request,render_template
import re
import functools

def validate_text_is_not_empty(text_input="text"):
    """
    Validate if text is not empty
    """

    def wrapper(func):
        @functools.wraps(func)
        def validate(*args, **kwrgs):
            text = request.get_json().get(text_input)

            text = text.strip()

            if text == "":
                return {"message": f"{text_input} text is invalid."}, 422

            return func(*args, **kwrgs)

        return validate

    return wrapper


def validate_text_regenerating_input(func):
    """
    Validate text that needs to be regenerated if it valid or not
    """

    def validate_regenerating_input(*args, **kwrgs):
        text = str(request.get_json().get("text"))

        text = text.strip()
        text = re.sub(r"\s+", " ", text)

        if text == "":
            return {"message": "Provided text is empty."}, 422
        if len(text.split()) < 20:
            return {"message": "Provided text is so smalle."}, 422

        return func(*args, **kwrgs)

    return validate_regenerating_input


def validate_uploaded_document(func):
    """
    Validate uploaded document if it is exists, valid, and its mimetype is `application/pdf` which located on the body of request and its name is `document`
    """

    @functools.wraps(func)
    def validate(*args, **kwrgs):
        if "document" not in request.files:
            return render_template('mindMap.html',errorMessage="please upload document"),422

        file = request.files.get("document")
        file_mimetype = file.mimetype

        if file_mimetype != "application/pdf":
            return render_template('mindMap.html',errorMessage="please upload PDF document"),422
        return func(*args, **kwrgs)

    return validate
