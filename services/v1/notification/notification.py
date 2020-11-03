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
        productHTML = "<tr>"
        for prod in productList:
            productHTML += "<td>" + prod["itemName"] + "</td><td>" + prod["qty"] + "</td><td>" + prod["price"] +  "</td><tr>"
    
        data = {
            'Messages': [
                {
                "From": {
                    "Email": "noreply@casafair.org",
                    "Name": "Casafair Notifications"
                },
                "To": [
                    {
                    "Email": email,
                    "Name": firstName + " " + lastName
                    }
                ],
                "Subject": "Casafair Confirmation: Order #" + orderId,
                "TextPart": "Your order has been placed successfully!",
                "HTMLPart": '<!DOCTYPE html><html lang="en"><head> <style>.center{text-align: center; margin-left: auto; margin-right: auto;}img{display: block; margin-left: auto; margin-right: auto; width: 50px;}table.orderTable{font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif; border: 1px solid #80257D; text-align: center;}table.orderTable td, table.orderTable th{border: 1px solid #AAAAAA; padding: 3px 2px;}table.orderTable tbody td{font-size: 13px; color: #80257D;}table.blueTable td, table.blueTable th{border: 1px solid #AAAAAA; padding: 3px 2px;}table.blueTable tbody td{font-size: 13px; color: #80257D;}</style></head><body> <div class="center"> <img src="https://avatars0.githubusercontent.com/u/71128513?s=200&v=4" alt="CasaFair logo"> <p>Hi ' + firstName + " " + lastName + '!</p><p> Thank you for choosing CasaFair! Your Order details are indicated below. </p><p>Your Order details</p><p>Order ID:' + orderId + '</p><table class="orderTable center"> <tr> <th>Item</th> <th>Qty</th> <th>Price</th> </tr>' + productHTML + '</table> </div></body></html>'
                
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