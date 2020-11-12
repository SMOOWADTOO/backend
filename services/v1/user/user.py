from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.mysql import BIGINT, TIMESTAMP, TINYINT, LONGTEXT, DATE, DATETIME
import hashlib, base64, time, datetime, jwt, json, uuid, os, boto3
from mimetypes import guess_extension
from urllib.request import urlretrieve, urlcleanup
from functools import wraps
from botocore.exceptions import ClientError, NoCredentialsError

app = Flask(__name__)
app.secret_key = os.environ["USER_SVC_SECRET_KEY"]
SECRET = app.secret_key
TIME_LIMIT = 10800
ALGO = "HS256"

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

# ======================================================================

# ====== API SETUP ======

# Rate limiter to prevent abuse and runaway Cloud usage; per IP Address
limiter = Limiter(app, key_func=get_ipaddr, default_limits=["100 per minute", "500 per hour", "1000 per day"])

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

# ====== USER TYPES =======

USER_TYPES = {
    "normal_user": 0, 
    "business_employee": 1, 
    "business_admin": 2, 
    "system_admin": 3
}

# ====== USER TYPES =======

# ====== AUTH HELPERS =======

def encodeJWT(payload, time):
    print(payload)
    expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
    payload.update({"exp": expiry})
    return jwt.encode(payload, SECRET, ALGO)

def checkAuthHeader(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "").split()

        invalid_msg = {
            "type": "error",
            "message": "Invalid token. Registration and / or authentication is required",
            "authenticated": False
        }

        expired_msg = {
            "type": "error",
            "message": "Expired token. Reauthentication is required.",
            "authenticated": False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, SECRET)
            
            user = UserLogin.query.filter_by(email=data["email"]).first()
            if not user:
                raise RuntimeError("User not found")

            return f(user, *args, **kwargs)

        except (jwt.ExpiredSignatureError, Exception) as e:
            expired_msg["debug"] = str(e)
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code

        except (jwt.InvalidTokenError, Exception) as e:
            invalid_msg["debug"] = str(e)
            return jsonify(invalid_msg), 401
            
    return _verify

# ====== AUTH HELPERS =======

########################################################################
# User Accounts object for the users
########################################################################

class UserLogin(db.Model):
    __tablename__ = "user_login"

    id = db.Column(BIGINT(20), primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(TINYINT(1), nullable=True)
    created = db.Column(TIMESTAMP(), nullable=True)
    updated = db.Column(TIMESTAMP(), nullable=True)

    def init(self, username, email, password):
        self.email = email
        self.username = username
        self.password = password

    def details(self):
        type_name = ""
        for user_type,num in USER_TYPES.items():
            if num == self.type:
                type_name = user_type

        return {"id": self.id, 
        "username": self.username,
        "email": self.email, 
        "type": type_name, 
        "created": self.created, 
        "updated": self.updated}

    def user_type(self):
        type_name = ""
        for user_type,num in USER_TYPES.items():
            if num == self.type:
                type_name = user_type
        return {"id": self.id, 
        "email": self.email, 
        "type": type_name}

##########
# METHODS
##########


@app.route("/user/check/<string:email>", methods=['GET'])
def checkEmailExists(email, json=True):
    user = UserLogin.query.filter_by(email=email).first()
    if user:
        if not json:
            return True, user
        return jsonify({"type": "success", "user": user.user_type(), "user_exists": True}), 200
    
    if not json:
        return False, ""
    return jsonify({"type": "error", "message": "User not found.", "user_exists": False}), 404

@app.route("/user/check/username/<string:username>", methods=['GET'])
def checkUsernameExists(username, json=True):
    user = UserLogin.query.filter_by(username=username).first()
    if user:
        if not json:
            return True, user
        return jsonify({"type": "success", "user": user.user_type(), "username_exists": True}), 200
    
    if not json:
        return False, ""
    return jsonify({"type": "error", "message": "User not found.", "username_exists": False}), 404

# Get user full details
@app.route("/user", methods=['GET'])
@checkAuthHeader
def findUserByEmail(user):
    user_details = user.details()
    return jsonify({"type": "success", "user": user_details}), 200

# Find User by ID
@app.route("/user/<int:id>", methods=['GET'])
def findUserByID(id):
    user = UserLogin.query.filter_by(id=id).first()
    if user:
        return jsonify({"type": "success", "user": user.details()}), 200
    return jsonify({"type": "error", "message": "User not found."}), 404

# Find User by username
@app.route("/user/username/<string:username>", methods=['GET'])
def findUserByUsername(username):
    user = UserLogin.query.filter_by(username=username).first()
    if user:
        return jsonify({"type": "success", "user": user.details()}), 200
    return jsonify({"type": "error", "message": "User not found."}), 404

# Create a new User
@app.route("/user/<string:user_type>", methods=['POST'])
def createUser(user_type):
    data = request.get_json()
    ts = time.gmtime()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', ts)
    data.update({"created": timestamp})

    if user_type in USER_TYPES:
        data["type"] = USER_TYPES[user_type]
    else:
        return jsonify(
            {"type": "error", 
            "message": "Invalid URL"}
        ), 404
    
    hashed_password = hashlib.md5(data["password"].encode('utf-8')).hexdigest()
    data["password"] = hashed_password

    if "firstName" in data and "lastName" in data:

        first_name = data["firstName"]
        del data["firstName"]

        last_name = data["lastName"]
        del data["lastName"]
    
    else:
        return jsonify(
            {"type": "error", 
            "message": "firstName and lastName fields missing.", 
            "debug": str(e)}
        ), 400

    user = UserLogin(**data)
    
    try:
        db.session.add(user)
        db.session.flush()
        createUserProfile(user.details()["id"], first_name, last_name)
        db.session.commit()
        
    except Exception as e:
        print(e)
        if type(e) == IntegrityError:
            return jsonify({
                "type": "error", 
                "message": "This email address exists.", 
                "debug": str(type(e))}
            ), 400

        return jsonify({
            "type": "error", 
            "message": "An error occurred when creating a new user.", 
            "debug": str(e)}
        ), 500

    return jsonify({"type": "success", "user": user.details()}), 201

# Authenticate user (login function)
@app.route("/user/authentication", methods=['POST'])
def authenticate():
    data = request.get_json()
    try:
        user = checkEmailExists(data['email'])
    
        if user[1] == 200:
            password_hashed = hashlib.md5(data['password'].encode('utf-8')).hexdigest()
            db_user = UserLogin.query.filter_by(email=data['email'], password=password_hashed).first()
            
            if db_user:
                print(db_user)
                db_profile = UserProfile.query.filter_by(userID=db_user.id).first()
                payload = db_user.details()
                del payload['created']
                del payload['updated']

                profile_payload = db_profile.details()
                
                payload.update(profile_payload)

                minimal_profile = db_profile.minimal_details()
                minimal_profile.update(db_user.details())

                del minimal_profile["userID"]

                access_jwt = encodeJWT(payload, TIME_LIMIT).decode('utf-8')
                
                return jsonify({"type": "success", "token": access_jwt, "user": minimal_profile}), 200
            else:
                return jsonify({"type": "error", "message": "Password incorrect."}), 403
        else:
            return jsonify({"type": "error", "message": "Login email not found."}), 404
    except Exception as e:
        return jsonify({"type": "error", "message": "Database might be offline.", "debug": str(e)}), 500

    return jsonify({"type": "error", "message": "Unknown error has occurred."}), 500

########################################################################

class UserProfile(db.Model):
    __tablename__ = "user_profile"

    userID = db.Column(BIGINT(20), primary_key=True)
    nric = db.Column(db.String(10), nullable=True)
    firstName = db.Column(db.String(255), nullable=True)
    lastName = db.Column(db.String(255), nullable=True)
    gender = db.Column(TINYINT(1), nullable=True)
    birthday = db.Column(DATETIME, nullable=True)
    profilePhotoURL = db.Column(db.String(255), nullable=True)
    description = db.Column(LONGTEXT, nullable=True)
    addressLine1 = db.Column(db.String(255), nullable=True)
    addressLine2 = db.Column(db.String(255), nullable=True)
    postalCode = db.Column(db.String(11), nullable=True)
    phoneNo = db.Column(db.String(15), nullable=True)
    telegramToken = db.Column(BIGINT(10), nullable=True)
    created = db.Column(TIMESTAMP(), nullable=True)
    updated = db.Column(TIMESTAMP(), nullable=True)

    def init(self, userID):
        self.userID = userID
        self.firstName = firstName
        self.lastName = lastName

    def details(self):
        birthday = None
        profilePhoto = None
        if self.birthday != None:
            birthday = self.birthday.strftime("%Y-%m-%d")

        if self.profilePhotoURL != None:
            profilePhoto = "https://s3.ap-southeast-1.amazonaws.com/casafair/" + self.profilePhotoURL
            
        return {
            "userID": self.userID,
            "nric": self.nric,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "birthday": birthday,
            "gender": self.gender,
            "profilePhotoURL": profilePhoto,
            "description": self.description, 
            "addressLine1": self.addressLine1, 
            "addressLine2": self.addressLine2, 
            "postalCode": self.postalCode, 
            "phoneNo": self.phoneNo, 
            "telegramToken": self.telegramToken
        }

    def minimal_details(self):
        return {
            "userID": self.userID,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "gender": self.gender,
            "phoneNo": self.phoneNo,
            "description": self.description
        }

##########
# METHODS
##########

# Create a new UserProfile
def createUserProfile(userID, firstName, lastName):
    data = {"userID": userID, "firstName": firstName, "lastName": lastName}
    ts = time.gmtime()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', ts)
    data.update({"created": timestamp})
    # **data represent the rest of the data
    user = UserProfile(**data)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"type": "error", "message": "An error occurred creating the user profile.", "debug": str(e)}), 500

# Get user full details
@app.route("/user/profile/me", methods=['GET'])
@checkAuthHeader
def getFullUserProfile(user):
    user_details = user.details()
    userID = user_details["id"]

    profile = UserProfile.query.filter_by(userID=userID).first()
    
    user_details.update(profile.details())
    del user_details["userID"]

    return jsonify({"type": "success", "user": user_details}), 200

# Find user profile by username
@app.route("/user/profile/<int:userID>", methods=['GET'])
def findProfileByUserID(userID):
    user = UserProfile.query.filter_by(userID=userID).first().details()
    login_user = UserLogin.query.filter_by(id=userID).first().details()
    user.update(login_user)
    if user:
        return jsonify({"type": "success", "user_profile": user}), 200
    return jsonify({"type": "error", "message": "User profile not found."}), 404

# update UserProfile by ID
# used by Account Settings page
@app.route("/user/profile", methods=['POST'])
@checkAuthHeader
def updateUserProfile(user):
    user_details = user.details()
    userID = user_details["id"]
    
    user = UserProfile.query.filter_by(userID=userID).first()

    if user:
        data = request.get_json()

        ts = time.gmtime()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', ts)
        data.update({"updated": timestamp})
        
        for key in data:
            if key == "birthday":
                data[key] = datetime.datetime.strptime(data[key], "%Y-%m-%dT%H:%M:%S.%fZ")
            
            #profile photo
            if key == "profilePhotoFile":
                if data["profilePhotoFile"] != "":
                    filename = uploadProfilePhoto(data[key], userID)
                    setattr(user, "profilePhotoURL", filename)
            # else:
            setattr(user, key, data[key])
        
        try:
            db.session.commit()
            return jsonify({"type": "success", "message": "Successfully updated"}), 201
        except Exception as e:
            reason = str(e)
            return jsonify({"type": "error", "message": "An error occurred updating the profile.", "debug": reason}), 500

    else:
        return jsonify({"type": "error", "message": "User profile not found."}), 404
    
    return jsonify({"type": "error", "message": "Server error. Could not update."}), 500

def uploadProfilePhoto(profile_photo_file, user_id):
    try:
        s3_image_name = "user/" + str(user_id) + "/"

        file_name, headers = urlretrieve(profile_photo_file)

        extension = guess_extension(headers.get_content_type())

        name_hashed = uuid.uuid4().hex + extension
        s3_image_name += name_hashed

        content_type = {}

        if extension == ".jpg":
            content_type = {"ContentType": "image/jpeg"}
            b64_image = profile_photo_file.replace("data:image/jpeg;base64,", "")
        elif extension == ".png":
            content_type = {"ContentType": "image/png"}
            b64_image = profile_photo_file.replace("data:image/png;base64,", "")

        S3_CLIENT.put_object(Body=base64.b64decode(b64_image), Bucket=BUCKET_NAME, Key=s3_image_name, ContentEncoding="base64", ContentType=content_type["ContentType"])
        return s3_image_name
    except Exception as e:
        raise

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001, debug=True)