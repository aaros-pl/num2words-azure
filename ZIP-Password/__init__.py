import logging

import azure.functions as func

import io
import base64
import py7zr
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # name = req.params.get('name')
    # pdf1 = req.params.get('pdf1')
    # pdf2 = req.params.get('pdf2')
    # if not pdf1 and not pdf2:
    # LOLOL
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    # else:
    #     pdf1 = req_body.get('pdf1')
    #     pdf2 = req_body.get('pdf2')

    file_in = req_body.get('file1')
    password = req_body.get('password')

    if file_in and password:
        file_in = io.BytesIO(base64.b64decode(file_in))
        # input1 = io.BytesIO(pdf1)
        # input2 = io.BytesIO(pdf2)
        file_in.seek(0)

        output = io.BytesIO()
        output.seek(0)

        with py7zr.SevenZipFile(output, 'w', password=password) as archive:
            archive.writeall(file_in, 'nazwa')

        output.seek(0)
        print("Successfully merged")

        return func.HttpResponse(output.getvalue(),
            headers={'Content-Type':'application/zip'}
            )
    else:
        return func.HttpResponse(
            json.dumps({
                'status': 'error',
                'content': 'Unable to parse pdf1 and pdf2'
            }),
            mimetype="application/json",
            status_code=400
            )
