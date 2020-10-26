from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
import json, os
import requests

app = Flask(__name__)

BASEURL = os.environ["HOMEBIZ_URL"]
CORS(app)

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
    url = BASEURL + "/product"
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
    url = BASEURL + "/shop/all"
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