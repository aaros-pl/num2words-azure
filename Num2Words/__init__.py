import logging

import azure.functions as func
from num2words import num2words as n2w
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass

    operation = req_body.get('operation')
    language = req_body.get('language')
    number = float(req_body.get('number'))
    currency_code = req_body.get('currency_code')

    if operation and language and number:
        if operation == "currency" and currency_code:
            try:
                output = n2w(number, lang=language, to=operation, currency=currency_code)
            except ValueError:
                pass
        else:
            output = n2w(number, lang=language, to=operation)

        return func.HttpResponse(
            json.dumps({
                'status': 'success',
                'content': output
            }),
            mimetype="application/json",
            status_code=200
            )
    else:
        return func.HttpResponse(
             "Error",
             status_code=400
        )
