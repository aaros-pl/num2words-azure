import logging

import azure.functions as func

from PyPDF4 import PdfFileMerger
import io
import base64
# from json import dumps
import json
import pdfrw


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # name = req.params.get('name')
    # pdf1 = req.params.get('pdf1')
    # pdf2 = req.params.get('pdf2')
    # if not pdf1 and not pdf2:
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    # else:
    #     pdf1 = req_body.get('pdf1')
    #     pdf2 = req_body.get('pdf2')
    pdf1 = req_body.get('pdf1')
    pdf2 = req_body.get('pdf2')

    if pdf1 and pdf2:
        input1 = io.BytesIO(base64.b64decode(pdf1))
        input2 = io.BytesIO(base64.b64decode(pdf2))
        # input1 = io.BytesIO(pdf1)
        # input2 = io.BytesIO(pdf2)
        input1.seek(0)
        input2.seek(0)

        output = io.BytesIO()
        merger = PdfFileMerger(output)

        # Próbujemy mergować pliki
        # łączenie, zapisywanie i zamykanie wirtualnego pliku
        merger.append(input1)
        merger.append(input2)
        merger.write(output)
        merger.close()
        # przeniesienie kursora na początek wirtualnego pliku
        output.seek(0)
        print("Successfully merged")
        # output64 = base64.b64encode(output.getvalue())
        # output64 = base64.b64encode(output.getvalue()).decode()
        # b_output = str(output.getvalue())[2:-1]
        # base_output = str(base64.b64encode(output.getvalue()))[2:-1]
        # return func.HttpResponse(
        #     json.dumps({
        #         'status': 'success',
        #         'content': base_output
        #     }),
        #     mimetype="application/json",
        #     status_code=200
        #     )

        return func.HttpResponse(output.getvalue(),
            headers={'Content-Type':'application/pdf'}
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
