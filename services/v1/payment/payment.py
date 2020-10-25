from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME
import time, datetime, json, os, requests, math, stripe, base64

app = Flask(__name__)

CORS(app)

# ======================================================================

# ====== API SETUP ======

stripe.api_key = os.environ["STRIPE_KEY"]

# Rate limiter to prevent abuse and runaway Cloud usage; per IP Address
limiter = Limiter(app, key_func=get_ipaddr, default_limits=["10000 per minute", "100 per hour", "300 per day"])

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

GST = 1.07

##########
# METHODS
##########

@app.route('/payment/calculate', methods=['POST'])
def calculatePayment(api_call=True, products=""):
    if api_call:
        try:
            data = request.get_json()
            products = data["products"]
        except Exception as e:
            return jsonify({
                "type": "error",
                "message": "Invalid parameters"
            }), 400

    total_amount = 0.0

    for product in products:
        total_amount += product["unitPrice"] * product["quantity"]

    final_amount = total_amount * GST

    if api_call:
        return jsonify({
            "preTax": total_amount,
            "amount": final_amount,
            "gst": final_amount - total_amount
        }), 200
    else:
        return final_amount


@app.route('/payment/session', methods=['POST'])
def beginPaymentSession():
    data = request.get_json()

    iat = datetime.datetime.utcnow()
    data["iat"] = str(iat)

    message = json.dumps(data)

    message_bytes = message.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    token = base64_bytes.decode('utf-8')

    return jsonify({"type": "success", "paymentToken": token}), 200

@app.route('/payment/intent', methods=['POST'])
def createIntent():
    try:
        data = request.get_json()

        decoded_token = base64.b64decode(data["paymentToken"].encode('utf-8'))
        token = decoded_token.decode('utf-8')

        payment_data = json.loads(token)

        iat = payment_data["iat"]
        iat = datetime.datetime.strptime(iat, "%Y-%m-%d %H:%M:%S.%f")

        now = datetime.datetime.utcnow()
        mins_elapsed_since_iat = math.ceil((now - iat).total_seconds() / 60)

        if mins_elapsed_since_iat > 1:
            return jsonify({"type": "error", "message": "Payment session has expired. Please refresh the page."})

        calculations = calculatePayment(False, payment_data["products"])

        amount_cents = int(calculations * 100)
        intent = stripe.PaymentIntent.create(
            amount = amount_cents,
            currency = "sgd",
            metadata = {
                "type": "WAD2",
                "data": json.dumps(payment_data["products"])
            },
        )

        return jsonify({
            "type": "success",
            "purchasedProducts": payment_data["products"],
            "iat": iat,
            "paymentIntentID": intent["id"],
            "amountPaid": amount_cents / 100
        }), 200

    except Exception as e:
        reason = str(e)
        return jsonify({"type": "error", "message": reason}), 403

# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7006, debug=True)