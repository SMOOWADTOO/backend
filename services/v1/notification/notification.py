from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
import base64, time, datetime, json, os, traceback
from mailjet_rest import Client

API_KEY = os.environ["MAILJET_API_KEY"]
API_SECRET = os.environ["MAILJET_API_SECRET"]

MAILJET = Client(auth=(API_KEY, API_SECRET), version='v3.1')

app = Flask(__name__)

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

@app.route("/notification/email", methods=["POST"])
def send_email():
    message = request.get_json()
    try:
        email = message['email']
        firstName = message['firstName']
        lastName = message['lastName']
        orderId = message['orderId']
        productList = message['productList']

        products = "<ul>"

        for product in productList:
            products += "<li>" + product + "</li>"

        products = "</ul>"

        data = {
            'Messages': [
                {
                "From": {
                    "Email": "noreply.casafair@gmail.com",
                    "Name": "Casafair Notifications"
                },
                "To": [
                    {
                    "Email": email,
                    "Name": firstName + " " + lastName
                    }
                ],
                "Subject": "Casafair Confirmation: Order #" + orderId,
                "HTMLPart": "Hi there, " + firstName + ". Your Order Id is " + orderId + ". You have bought the following: <br>" + products
                
                }
            ]
        }
        result = MAILJET.send.create(data=data)
        return jsonify({"type": "success", "message": "Successfully sent an email"}), 200
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {"type": "error", 
            "message": "An error occurred sending the notification.",
            "debug": str(e)}
        ), 500

# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7007, debug=True)