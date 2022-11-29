import requests
from flask import make_response
import base64
from python.common.config import Config
import json


def render(*html):
    """
    Calls the PDF rendering microservice to convert html into
    a PDF file.
    """
    PDF_URL =Config.PDF_SERVICE_URL
   
    response = requests.post(
        "{}/pdf?bootstrap=true".format(PDF_URL), data=html[0].encode("utf-8"), stream=True
    )

    return response.content


def generate_pdf(**kwargs) -> tuple:
    # print("____________")
    try:
        html = kwargs['message']['icbc_submission']['pdf']                
        pdf_content = render(html)
        base64_encode_pdf_string = base64.b64encode(pdf_content).decode('utf-8')
        # # TODO remove for oc
        # file_content = base64.b64decode(base64_encode_pdf_string)
        # with open("test.pdf","wb") as f:
        #     f.write(file_content)
        # print("____PDF file is ready!") 
               
        kwargs['message']['icbc_submission']['pdf']=base64_encode_pdf_string
        
    except Exception as e:
        return False, kwargs
    return True, kwargs