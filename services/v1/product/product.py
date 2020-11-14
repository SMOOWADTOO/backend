from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME, INTEGER
import base64, time, datetime, json, os, boto3, uuid
import traceback
from mimetypes import guess_extension
from urllib.request import urlretrieve, urlcleanup
from botocore.exceptions import ClientError, NoCredentialsError

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

# ======= AWS SETUP =======

BUCKET_NAME = os.environ["S3_BUCKET_URL"]
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]

S3_CLIENT = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

# ======= AWS SETUP =======

# ====== API SETUP ======

# Rate limiter to prevent abuse and runaway Cloud usage; per IP Address
limiter = Limiter(app, key_func=get_ipaddr, default_limits=["100 per minute", "2000 per hour"])

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
    productPhotoURL = db.Column(db.String(255), nullable=True)
    unitPrice = db.Column(db.Float, nullable=False)

    def __init__(self, shopId, productName, productDesc, unitPrice, productPhotoURL = ""):
        self.shopId = shopId
        # self.productId = productId # no need since productId is set with autoincrement=True
        self.productName = productName
        self.productDesc = productDesc
        self.unitPrice = unitPrice
        self.productPhotoURL = productPhotoURL
    
    def details(self):
        productPhoto = None
        if self.productPhotoURL != None and self.productPhotoURL != "":
            productPhoto = "https://s3.ap-southeast-1.amazonaws.com/casafair/" + self.productPhotoURL

        return {
            "shopId": self.shopId,
            "productId": self.productId,
            "productName": self.productName,
            "productDesc": self.productDesc,
            "unitPrice": self.unitPrice,
            "productPhotoURL": productPhoto
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
        else:
            return jsonify({"products": [], "type": "success"}), 200
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

        productPhoto = product_obj["productPhotoFile"]
        
        new_product = Product(shopId, productName, productDesc, unitPrice)
        db.session.add(new_product)

        # add new photo
        if productPhoto != "":
            db.session.commit()
            product = new_product.details()

            product_id = product["productId"]
            product = Product.query.filter_by(productId=product_id).first()

            filename = uploadProductPhoto(productPhoto, product_id)
            
            setattr(product, "productPhotoURL", filename)
            db.session.commit()

        else:
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

# Add product
@app.route("/product/edit", methods=["POST"])
def editProduct():
    try:
        product_obj = request.get_json()
        product_id = product_obj["productId"]

        product = Product.query.filter_by(productId=product_id).first()

        ts = time.gmtime()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', ts)

        if product:
            for k,v in product_obj.items():
                # product photo
                if k == "productPhotoFile":
                    if v != "":
                        filename = uploadProductPhoto(v, product_id)
                        setattr(product, "productPhotoURL", filename)
                
                setattr(product, k, v)

            db.session.commit()
        else:
            return jsonify({"type": "error", "message": "Product not found."}), 404
        return jsonify({"type": "success", "product": product.details(), "message": "Successfully updated your product!"}), 200
    
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when editing the product.", 
            "debug": str(e)}
        ), 500

def uploadProductPhoto(product_photo_file, product_id):
    try:
        s3_image_name = "product/" + str(product_id) + "/"

        file_name, headers = urlretrieve(product_photo_file)

        extension = guess_extension(headers.get_content_type())

        name_hashed = uuid.uuid4().hex + extension
        s3_image_name += name_hashed

        content_type = {}

        if extension == ".jpg":
            content_type = {"ContentType": "image/jpeg"}
            b64_image = product_photo_file.replace("data:image/jpeg;base64,", "")
        elif extension == ".png":
            content_type = {"ContentType": "image/png"}
            b64_image = product_photo_file.replace("data:image/png;base64,", "")

        S3_CLIENT.put_object(Body=base64.b64decode(b64_image), Bucket=BUCKET_NAME, Key=s3_image_name, ContentEncoding="base64", ContentType=content_type["ContentType"])
        return s3_image_name
    except Exception as e:
        raise

# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7004, debug=True)