from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME, INTEGER
import base64, time, datetime, json, uuid, os, boto3
import traceback
from mimetypes import guess_extension
from urllib.request import urlretrieve, urlcleanup

app = Flask(__name__)

DB_BASE_URL = os.environ["ORDER_DB_BASE_URL"]

app.config['SQLALCHEMY_DATABASE_URI'] = DB_BASE_URL + '/order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
 
db = SQLAlchemy(app)
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

########################################################################
# homebiz_order --- TABLE Order
########################################################################

class Order(db.Model):
    __tablename__ = "orders"

    orderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    pickupAddress = db.Column(LONGTEXT, nullable=False)
    deliveryAddress = db.Column(LONGTEXT, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    paid = db.Column(db.Boolean, nullable=False)
    createdAt = db.Column(TIMESTAMP(), nullable=False)

    def __init__(self, username, pickupAddress, deliveryAddress, completed, paid):
        # self.shopId = shopId # no need since shopId is set with autoincrement=True
        self.username = username
        self.pickupAddress = pickupAddress
        self.deliveryAddress = deliveryAddress
        self.completed = completed
        self.paid = paid
    
    def details(self):
        return {
            "orderId": self.orderId,
            "username": self.username,
            "pickupAddress": self.pickupAddress,
            "deliveryAddress": self.deliveryAddress,
            "completed": self.completed,
            "paid": self.paid,
            "createdAt": self.createdAt,
        }

class OrderDetails(db.Model):
    __tablename__ = "orderDetails"

    orderDetailId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderId = db.Column(db.Integer, nullable=False)
    productId = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    createdAt = db.Column(TIMESTAMP(), nullable=False)

    def __init__(self, orderId, productId, price, quantity, total):
        # self.shopId = shopId # no need since shopId is set with autoincrement=True
        self.orderId = orderId
        self.productId = productId
        self.price = price
        self.quantity = quantity
        self.total = total
    
    def details(self):
        return {
            "orderDetailId": self.orderDetailId,
            "orderId": self.orderId,
            "productId": self.productId,
            "price": self.price,
            "quantity": self.quantity,
            "total": self.total,
            "createdAt": self.createdAt,
        }

##########
# METHODS
##########

# Get all orders
@app.route("/order/all", methods=['GET'])
def getAllOrders():
    result = {"orders": []}
    try:
        orders = Order.query.all()
        for order in orders:
            data = order.details()
            orderDetails = OrderDetails.query.filter_by(orderId=data['orderId'])
            od = []
            total = 0
            for orderDetail in orderDetails:
                total += orderDetail.total
                od.append(orderDetail.details())
            data['order_details'] = od
            data['total'] = total
            result['orders'].append(data)
        result['type'] = "success"
        return result, 200
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting all orders.", 
            "debug": str(e)}
        ), 404

# Get order and order details of a specific order
@app.route("/order/<string:orderId>", methods=['GET'])
def getOrderByOrderId(orderId):
    result = {}
    try:
        order = Order.query.filter_by(orderId=orderId).first()
        if order:
            data = order.details()
            orderDetails = OrderDetails.query.filter_by(orderId=orderId)
            od = []
            total = 0
            for orderDetail in orderDetails:
                total += orderDetail.total
                od.append(orderDetail.details())
            data['order_details'] = od
            data['total'] = total
            result['order'] = data
            result['type'] = 'success'
            return result, 200
        return {
            "type": "error",
            "message": "orderId does not exist."
        }, 404
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting all orders.", 
            "debug": str(e)}
        ), 500

# Get order and order details of a specific username
@app.route("/order/user/<string:username>", methods=['GET'])
def getOrderByUser(username):
    result = {}
    try:
        order = Order.query.filter_by(username=username).first()
        if order:
            data = order.details()
            orderDetails = OrderDetails.query.filter_by(orderId=order.orderId)
            od = []
            total = 0
            for orderDetail in orderDetails:
                total += orderDetail.total
                od.append(orderDetail.details())
            data['order_details'] = od
            data['total'] = total
            result['order'] = data
            result['type'] = 'success'
            return result, 200
        return {
            "type": "error",
            "message": "User has no orders."
        }, 404
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting all orders.", 
            "debug": str(e)}
        ), 500

# Create new order
@app.route("/order/create", methods=["POST"])
def createOrder():
    try:
        order_obj = request.get_json()
        username = order_obj.get("username")
        if username is None:
            return jsonify({"type": "error", "message": "username is required"}), 500
        orderDetails = order_obj.get("order_details")
        if orderDetails is None:
            return jsonify({"type": "error", "message": "order_details is required"}), 500
        if type(orderDetails) != list:
            return jsonify({"type": "error", "message": "order_details need to be a list"}), 500

        try:
            max_id = db.session.query(db.func.max(Order.orderId)).scalar()
            orderId = max_id + 1
        except:
            orderId = 1

        try:
            for orderDetail in orderDetails:
                newOrderDetail = OrderDetails(orderId, **orderDetail)
                db.session.add(newOrderDetail)
                db.session.commit()
        except:
            return jsonify({"type": "error", "message": "Error inputting order_details data into database"}), 500

        del order_obj['order_details']

        new_order = Order(**order_obj)
        db.session.add(new_order)
        db.session.commit()

        result = {}
        result['order'] = getOrderByOrderId(orderId)[0]['order']
        result['type'] = 'success'

        return jsonify(result), 201
    
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when creating a new order.", 
            "debug": str(e)}
        ), 500

# Edit order details
@app.route("/order/edit", methods=["POST"])
def editOrder():
    try:
        order_obj = request.get_json()
        orderId = order_obj.get("orderId")
        if orderId is None:
            return jsonify({"type": "error", "message": "orderId is required"}), 500
        order = Order.query.filter_by(orderId=orderId).first()
        if order is None:
            return {
                "type": "error",
                "message": "orderId " + str(orderId) + " does not exist."
            }, 500

        username = order_obj.get("username")
        if username is None:
            return jsonify({"type": "error", "message": "username is required"}), 500
        
        forbidden_fields = ['orderId', 'username', 'createdAt', 'updatedAt']
        for k,v in order_obj.items():
            if k not in forbidden_fields:
                setattr(order, k, v)
        setattr(order, 'updatedAt', datetime.datetime.now())

        db.session.commit()
        return jsonify({"type": "success", "order": order.details()}), 201
    
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when editing order",
            "debug": str(e)}
        ), 500

# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7003, debug=True)