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

DB_BASE_URL = os.environ["USER_DB_BASE_URL"]

app.config['SQLALCHEMY_DATABASE_URI'] = DB_BASE_URL + '/homebiz_category'
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
# homebiz_category --- TABLE Category
########################################################################

class Category(db.Model):
    __tablename__ = "category"

    categoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoryName = db.Column(db.String(255), nullable=False)

    def __init__(self, categoryId, categoryName):
        self.categoryName = categoryName

    
    def details(self):
        return {
            "categoryId": self.categoryId,
            "categoryName": self.categoryName,
        }

##########
# METHODS
##########

# Get all products
@app.route("/category", methods=['GET'])
def getAllProducts():
    try:
        return {
            'categories': [
                category.details() for category in Category.query.all()
            ]
        }, 200
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when getting all categories.", 
            "debug": str(e)}
        ), 500

# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7006, debug=True)