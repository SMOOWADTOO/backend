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
    try:
        url = "https://developers.onemap.sg/commonapi/search?searchVal=" + postal_code + "&returnGeom=Y&getAddrDetails=Y"
        result = requests.get(url).json()
        if result["found"] == 0:
            return jsonify({"message": "Not found!"}), 404
        else:
            address = result["results"][0]
            return jsonify({"address": address, "type": "success"}), 200
    except Exception as e:
        return jsonify({"debug": str(e), "type": "success", "message": "Unable to fetch address from API due to an internal error."}), 200


# Rename of .py files easily
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7008, debug=True)