from flask import Flask, request, jsonify
from flask_cors import CORS
import os, shutil, time, datetime, json, pathlib, boto3, uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from botocore.exceptions import ClientError
from google.cloud import storage

app = Flask(__name__)

CORS(app)

# ======================================================================

# ======= AWS SETUP =======

# idk if we should use AWS or GCP?

AWS_S3_CLIENT = boto3.client("s3")
AWS_S3_RESOURCE = boto3.resource("s3")
BUCKET_NAME = ""

# ======= AWS SETUP =======

# ======= GCP SETUP =======

# GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
# BUCKET_NAME = os.environ["BUCKET_NAME"]
# STORAGE_CLIENT = storage.Client()
# BUCKET = STORAGE_CLIENT.bucket(BUCKET_NAME)

# ======= GCP SETUP =======

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

# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001, debug=True)