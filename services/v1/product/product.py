from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME, INTEGER
import base64, time, datetime, json, os
import traceback

app = Flask(__name__)

DB_BASE_URL = os.environ["DB_BASE_URL"]
DB_NAME = os.environ["USER_DB_NAME"]

app.config['SQLALCHEMY_DATABASE_URI'] = DB_BASE_URL + "/" + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
 
db = SQLAlchemy(app)
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

########################################################################
# homebiz_product --- TABLE Product
########################################################################

class Product(db.Model):
    __tablename__ = "product"

    shopId = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productName = db.Column(db.String(255), nullable=False)
    productDesc = db.Column(db.String(255), nullable=False)
    unitPrice = db.Column(db.Float, nullable=False)

    def __init__(self, shopId, productName, productDesc, unitPrice):
        self.shopId = shopId
        # self.productId = productId # no need since productId is set with autoincrement=True
        self.productName = productName
        self.productDesc = productDesc
        self.unitPrice = unitPrice
    
    def details(self):
        return {
            "shopId": self.shopId,
            "productId": self.productId,
            "productName": self.productName,
            "productDesc": self.productDesc,
            "unitPrice": self.unitPrice,
        }

##########
# METHODS
##########

# Get all products
@app.route("/product", methods=['GET'])
def getAllProducts():
    try:
        return jsonify({
            'products': [
                product.details() for product in Product.query.all()
            ]
        }), 200
    except Exception as e:
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting all products.", 
            "debug": str(e)}
        ), 500

# Get products by shop id
@app.route("/product/by_store/<string:shopId>", methods=['GET'])
def getProductsByShopId(shopId):
    try:
        # data = Product.query.filter_by(shopId=shopId)
        products = Product.query.filter_by(shopId=shopId)
        if len(products.all()) != 0:
            return jsonify({"products": [product.details() for product in products], "type": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting products by shop ID.", 
            "debug": str(e)}
        ), 500

# Get products by product id
@app.route("/product/<string:productID>", methods=['GET'])
def getProductByID(productID):
    try:
        # data = Product.query.filter_by(shopId=shopId)
        product = Product.query.filter_by(productId=productID).first()
        return jsonify({"product": product.details(), "type": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting products by Product ID.", 
            "debug": str(e)}
        ), 500

# Add product
@app.route("/product/add", methods=["POST"])
def addProduct():
    try:
        product_obj = request.get_json()
        shopId = product_obj["shopId"]
        productName = product_obj["productName"]
        productDesc = product_obj["productDesc"]
        unitPrice = product_obj["unitPrice"]
        
        new_product = Product(shopId, productName, productDesc, unitPrice)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"type": "success", "product": new_product.details()}), 201
    
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when adding a new product.", 
            "debug": str(e)}
        ), 500



# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7004, debug=True)