from flask import Flask, request, jsonify
from flask_cors import CORS
# import jwt
import json
import requests

app = Flask(__name__)
CORS(app)

########################################################################
# ONEMAP API
API_KEYS = ""

########################################################################

@app.route("/general/map/address/<string:postal_code>")
def getAddress(postal_code):
    url = "https://developers.onemap.sg/commonapi/search?searchVal=" + postal_code + "&returnGeom=Y&getAddrDetails=Y"
    result = requests.get(url).json()
    if result["found"] == 0:
        return jsonify({"message": "Not found!"}), 404
    else:
        address = result["results"][0]
        return address


# Rename of .py files easily
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7008, debug=True)