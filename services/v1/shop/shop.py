from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME, INTEGER
import base64, time, datetime, json, uuid, os
import traceback

app = Flask(__name__)

DB_BASE_URL = os.environ["SHOP_DB_BASE_URL"]

app.config['SQLALCHEMY_DATABASE_URI'] = DB_BASE_URL + '/shop'
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
# homebiz_shop --- TABLE Shop
########################################################################

class Shop(db.Model):
    __tablename__ = "shop"

    shopId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    shopName = db.Column(db.String(255), nullable=False)
    shopDesc = db.Column(LONGTEXT, nullable=True)
    shopImageURL = db.Column(LONGTEXT, nullable=True)
    contactNo = db.Column(db.String(30), nullable=True)
    address = db.Column(LONGTEXT, nullable=True)
    email = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(TIMESTAMP(), nullable=False)
    updatedAt = db.Column(TIMESTAMP(), nullable=False)

    def __init__(self, username, shopName, shopDesc=None, shopImageURL=None, contactNo=None, address=None, email=None, website=None):
        # self.shopId = shopId # no need since shopId is set with autoincrement=True
        self.username = username
        self.shopName = shopName
        self.shopDesc = shopDesc
        self.shopImageURL = shopImageURL
        self.contactNo = contactNo
        self.address = address
        self.email = email
        self.website = website
    
    def details(self):
        return {
            "shopId": self.shopId,
            "username": self.username,
            "shopName": self.shopName,
            "shopDesc": self.shopDesc,
            "shopImageURL": self.shopImageURL,
            "contactNo": self.contactNo,
            "address": self.address,
            "email": self.email,
            "website": self.website,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }

##########
# METHODS
##########

# Get all products
@app.route("/shop/all", methods=['GET'])
def getAllShops():
    try:
        return {
            'shops': [
                shop.details() for shop in Shop.query.all()
            ], 
            'type': 'success'
        }, 200
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting all shops.", 
            "debug": str(e)}
        ), 404

# Get shop details of a specific shop
@app.route("/shop/<string:shopId>", methods=['GET'])
def getShopByShopId(shopId):
    try:
        # data = Product.query.filter_by(shopId=shopId)
        shop = Shop.query.filter_by(shopId=shopId).first()
        if shop:
            return {
                "shop": shop.details(),
                'type': 'success'
            }, 200
        return {
            "type": "error",
            "message": "shopId " + shopId + " does not exist."
        }, 404
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting all shops.", 
            "debug": str(e)}
        ), 500

# Create new shop
@app.route("/shop/create", methods=["POST"])
def createShop():
    try:
        shop_obj = request.get_json()
        username = shop_obj.get("username")
        if username is None:
            return jsonify({"type": "error", "message": "username is required"}), 500
        shopName = shop_obj.get("shopName")
        if shopName is None:
            return jsonify({"type": "error", "message": "shopName is required"}), 500
        
        new_shop = Shop(**shop_obj)
        db.session.add(new_shop)
        db.session.commit()
        return jsonify({"type": "success", "shop": new_shop.details()}), 201
    
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when creating a new shop.", 
            "debug": str(e)}
        ), 500

# Edit shop details
@app.route("/shop/edit", methods=["POST"])
def editShop():
    try:
        shop_obj = request.get_json()
        shopId = shop_obj.get("shopId")
        if shopId is None:
            return jsonify({"type": "error", "message": "shopId is required"}), 500
        shop = Shop.query.filter_by(shopId=shopId).first()
        if shop is None:
            return {
                "type": "error",
                "message": "shopId " + str(shopId) + " does not exist."
            }, 500

        username = shop_obj.get("username")
        if username is None:
            return jsonify({"type": "error", "message": "username is required"}), 500
        
        forbidden_fields = ['shopId', 'username', 'createdAt', 'updatedAt']
        for k,v in shop_obj.items():
            if k not in forbidden_fields:
                setattr(shop, k, v)
        setattr(shop, 'updatedAt', datetime.datetime.now())

        db.session.commit()
        return jsonify({"type": "success", "shop": shop.details()}), 201
    
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when editing shop",
            "debug": str(e)}
        ), 500

# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002, debug=True)