from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME
import base64, time, datetime, json, uuid, os, boto3
from mimetypes import guess_extension
from urllib.request import urlretrieve, urlcleanup
import requests

app = Flask(__name__)

# DB_BASE_URL = os.environ["USER_DB_BASE_URL"]
IPADDR = os.environ["HOMEBIZ_DEPLOYED_IPADDR"]

# app.config['SQLALCHEMY_DATABASE_URI'] = DB_BASE_URL + '/homebiz_user'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_POOL_SIZE'] = 100
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
 
# db = SQLAlchemy(app)
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

##########
# METHODS
##########

# Search for product
@app.route("/search/product/<string:term>", methods=['GET'])
def searchProduct(term):
    result = []
    port = 7004
    url = IPADDR + str(port) + "/product"
    data = requests.get(url).json()
    products = data['products']
    for product in products:
        name = product['productName']
        if term.lower() in name.lower():
            result.append(product)
    return jsonify(result), 200

# Search for shop
@app.route("/search/shop/<string:term>", methods=['GET'])
def searchShop(term):
    result = []
    port = 7002
    url = IPADDR + str(port) + "/shop/all"
    data = requests.get(url).json()
    shops = data['shops']
    for shop in shops:
        name = shop['shopName']
        if term.lower() in name.lower():
            result.append(shop)
    return jsonify(result), 200

# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7009, debug=True)