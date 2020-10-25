from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME, INTEGER
import base64, time, datetime, json, uuid, os, boto3
import traceback
from mimetypes import guess_extension
from urllib.request import urlretrieve, urlcleanup

from mailjet_rest import Client
api_key = 'd40aa83b8cef8702e46e989be6a4a4a3'
api_secret = '475d12e035aa2552b5472faca6df8fe8'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


app = Flask(__name__)

CORS(app)

# ======================================================================

# ======= AWS SETUP =======

AWS_S3_CLIENT = boto3.client("s3")
AWS_S3_RESOURCE = boto3.resource("s3")
BUCKET_NAME = ""

# ======= AWS SETUP =======

# ======================================================================

# ====== API SETUP ======

# Rate limiter to prevent abuse and runaway Cloud usage; per IP Address
limiter = Limiter(app, key_func=get_ipaddr, default_limits=["10 per minute", "100 per hour", "300 per day"])

# Default error handling messages
@app.errorhandler(404)
def errorHandler(e):
    return jsonify({"type": "error", "message": "Address not found."}), 404

@app.errorhandler(405)
def methodNotAllowedHandler(e):
    return jsonify({"type": "error", "message": "Method not allowed."}), 405

@app.errorhandler(429)
def ratelimitHandler(e):
    return jsonify({"type": "error", "message": "Rate limit exceeded %s" % e.description}), 429

@app.errorhandler(500)
def unexpectedExceptionHandler(e):
    return jsonify({"type": "error", "message": "An unexpected exception occurred: %s" % e.description}), 500

# ====== API SETUP ======

def send_email():
    message = {
        'email': 'ptvvo.2018@sis.smu.edu.sg',
        'name': 'Vi',
        'orderId': '1',
        'productList': 'Toothbrush, Yam cake'
    }
    email = message['email']
    name = message['name']
    orderId = message['orderId']
    productList = message['productList']

    data = {
    'Messages': [
        {
        "From": {
            "Email": "ptvvo.2018@sis.smu.edu.sg",
            "Name": "CasaFair"
        },
        "To": [
            {
            "Email": "ptvvo.2018@sis.smu.edu.sg",
            "Name": "Vi"
            }
        ],
        "Subject": "Order Confirmation",
        "TextPart": "My first Mailjet email",
        "HTMLPart": "Hi, " + name + ". Your Order Id is " + orderId + ". You have bought " + productList
        
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print (result.status_code)
    print (result.json())

# ======================================================================

if __name__ == '__main__':
    print("This is " + os.path.basename(__file__) + ": sending an email...")
    send_email()