from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME, INTEGER, DOUBLE
# import hashlib, base64, time, datetime, jwt, json, uuid, os, boto3
from mimetypes import guess_extension
from urllib.request import urlretrieve, urlcleanup

app = Flask(__name__)

DB_BASE_URL = os.environ["USER_DB_BASE_URL"]

app.config['SQLALCHEMY_DATABASE_URI'] = DB_BASE_URL + '/homebiz_product'
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
# homebiz_product --- TABLE Product
########################################################################

class Product(db.Model):
    __tablename__ = "product"

    shop_id = db.Column(INTEGER(11), primary_key=True)
    product_id = db.Column(INTEGER(11), primary_key=True)
    product_name = db.Column(VARCHAR(255), nullable=False)
    product_desc = db.Column(VARCHAR(255), nullable=False)
    unit_price = db.Column(DOUBLE(scale=2), nullable=False)

    def init(self, shop_id, product_id, product_name, product_desc, unit_price):
        self.shop_id = shop_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_desc = product_desc
        self.unit_price = unit_price
    
    def details(self):
        return {
            "shop_id": self.shop_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_desc": self.product_desc,
            "unit_price": self.unit_price,
        }

##########
# METHODS
##########

# Get all products
@app.route("/product", methods=['GET'])
def getAllProducts():
    try:
        return {
            'products': [
                product.json() for product in Product.query.all()
            ]
        }, 200
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting all products.", 
            "debug": str(e)}
        ), 500

# Get products by shop id
@app.route("/product/<string:shopId>", methods=['GET'])
def getProductsByShopId(shopId):
    try:
        # data = Product.query.filter_by(shopId=shopId)
        products = Product.query.filter_by(shopId=shopId)
        if len(products.all()) != 0:
            return {"products": [product.json() for product in products], "status": 200} 
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting products by shop ID.", 
            "debug": str(e)}
        ), 500

# Add product
@app.route("/product/add", methods=["POST"])
def addProduct():
    try:
        product_obj = request.get_json()
        shop_id = product_obj["shopId"]
        # product_id = product_obj["product_id"] # AUTO INCREMENT
        product_desc = product_obj["productDesc"]
        unit_price = product_obj["unitPrice"]
        # TODO: see if putting None for product_id work or not
        new_product = Product(shop_id, None, product_desc, unit_price)
        db.session.add(new_product)
        db.session.commit()
    
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when adding a new product.", 
            "debug": str(e)}
        ), 500

    return jsonify({"type": "success", "product": new_product.details()}), 201


# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7004, debug=True)