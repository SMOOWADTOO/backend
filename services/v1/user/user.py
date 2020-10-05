from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME
import hashlib, base64, time, datetime, jwt, json, uuid, os, boto3
from mimetypes import guess_extension
from urllib.request import urlretrieve, urlcleanup

app = Flask(__name__)

DB_BASE_URL = os.environ["USER_DB_BASE_URL"]

app.config['SQLALCHEMY_DATABASE_URI'] = DB_BASE_URL + '/homebiz_user'
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
# User Accounts object for the users
########################################################################

class UserLogin(db.Model):
    __tablename__ = "user_login"

    user_id = db.Column(BIGINT(20), primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(TINYINT(1), nullable=True)
    created_at = db.Column(TIMESTAMP(), nullable=True)
    updated_at = db.Column(TIMESTAMP(), nullable=True)

    def init(self, email, password):
        self.email = email
        self.password = password

    def details(self):
        return {"user_id": self.user_id, 
        "email": self.email, 
        "user_type": self.user_type, 
        "created_at": self.created_at, 
        "updated_at": self.updated_at}

    def user_type(self):
        return {"user_id": self.user_id, 
        "email": self.email, 
        "user_type": self.user_type}

##########
# METHODS
##########

# Create a new User
@app.route("/user/create", methods=['POST'])
def createUser():
    data = request.get_json()
    ts = time.gmtime()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', ts)
    data.update({"created_at": timestamp})
    
    hashed_password = hashlib.md5(data["password"].encode('utf-8')).hexdigest()
    data["password"] = hashed_password

    first_name = data["first_name"]
    del data["first_name"]

    last_name = data["last_name"]
    del data["last_name"]

    user = UserLogin(**data)
    
    try:
        
        db.session.add(user)
        db.session.flush()
        # createUserProfile(user.details()["user_id"], first_name, last_name)
        db.session.commit()
        
    except Exception as e:
        print(e)
        return jsonify(
            {"type": "error", 
            "message": "An error occurred when creating a new user.", 
            "debug": str(e)}
        ), 500

    return jsonify({"type": "success", "user": user.details()}), 201

# ======================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001, debug=True)