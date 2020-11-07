from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME, INTEGER
import base64, time, datetime, json, uuid, os
import traceback
from mimetypes import guess_extension
from urllib.request import urlretrieve, urlcleanup

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
limiter = Limiter(app, key_func=get_ipaddr, default_limits=["500 per minute", "10000 per hour", "1000000 per day"])

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

class Review(db.Model):
    __tablename__ = "review"

    reviewId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shopId = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    reviewDetail = db.Column(LONGTEXT, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    publishedTime = db.Column(db.DateTime(), nullable=False)

    # init doesn't need to include reviewId and publishedTime
    # ---- reviewId is auto incremented
    # ---- publishedTime is CURRENT_TIMESTAMP 
    def __init__(self, shopId, orderId, productId, username, title, reviewDetail, rating):
        self.shopId = shopId
        self.orderId = orderId
        self.productId = productId
        self.username = username
        self.title = title
        self.reviewDetail = reviewDetail
        self.rating = rating
    
    def details(self):
        return {
            "reviewId": self.reviewId,
            "shopId": self.shopId,
            "orderId": self.orderId,
            "productId": self.productId,
            "username": self.username,
            "title": self.title,
            "reviewDetail": self.reviewDetail,
            "rating": self.rating,
            "publishedTime": self.publishedTime
        }

##########
# METHODS
##########

# Get all reviews
@app.route("/review", methods=['GET'])
def getAllReviews():
    try:
        return {
            'reviews': [
                review.details() for review in Review.query.all()
            ]
        }, 200
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting all reviews.", 
            "debug": str(e)}
        ), 500

# Get reviews by shop id
@app.route("/review/<string:shopId>", methods=['GET'])
def getReviewsByShopId(shopId):
    try:
        reviews = Review.query.filter_by(shopId=shopId)
        if len(reviews.all()) != 0:
            return {"reviews": [review.details() for review in reviews], "status": "success"}, 200
        return {"reviews": [], "status": "success"}, 200
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting reviews by shop ID.", 
            "debug": str(e)}
        ), 500

# Get reviews by product id
@app.route("/review/<string:productId>", methods=['GET'])
def getReviewsByProductId(productId):
    try:
        reviews = Review.query.filter_by(productId=productId)
        if len(reviews.all()) != 0:
            return {"reviews": [review.details() for review in reviews], "status": "success"} 
        return {"reviews": [], "status": "success"}, 200
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting reviews by shop ID.", 
            "debug": str(e)}
        ), 500

# Check if order has been reviewed
@app.route("/review/done/<string:orderId>", methods=['GET'])
def isReviewed(orderId):
    try:
        reviews = Review.query.filter_by(orderId=orderId)
        if len(reviews.all()) != 0:
            return {"isReviewed": True, "orderId": orderId, "status": 200} 
        return {"isReviewed": False, "orderId": orderId, "status": 200} 
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting reviews by shop ID.", 
            "debug": str(e)}
        ), 500

# Add review
@app.route("/review/add", methods=["POST"])
def addReview():
    try:
        review_obj = request.get_json()
        shopId = review_obj["shopId"]
        orderId = review_obj["orderId"]
        productId = review_obj["productId"]
        username = review_obj["username"]
        title = review_obj["title"]
        reviewDetail = review_obj["reviewDetail"]
        rating = review_obj["rating"]
        # publishedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(publishedTime)

        new_review = Review(shopId, orderId, productId, username, title, reviewDetail, rating)
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"type": "success", "review": new_review.details()}), 201
    
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when adding a new review.", 
            "debug": str(e)}
        ), 500

# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7005, debug=True)