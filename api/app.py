import json
import os
from os.path import join, dirname
from datetime import datetime, timedelta, date
from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo, MongoClient
import flask_monitoringdashboard as dashboard
from dotenv import load_dotenv
from bson.json_util import dumps

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from handlers.register import Register
from handlers.login import Login
from handlers.topup import Topup
from handlers.payment import Payment
from handlers.transfer import Transfer
from handlers.transaction import Transaction
from handlers.profile import Profile

app = Flask(__name__)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app.config["JWT_SECRET_KEY"] = "36145479DB6E2DBE7DF7B56B7EC82"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

mongo = MongoClient("localhost", 27017)
db = mongo.db

# monitoring
dashboard.bind(app)


@app.route('/register', methods = ['POST'])
def register():
    handler = Register(db)

    result = handler.regist()
    response_wrapper = Response(result)
    response_wrapper.headers['Content-Type'] = 'application/json'
    return response_wrapper

@app.route('/login', methods = ['POST'])
def login():
    handler = Login(db)

    result = handler.login()

    returns = {}
    req_body = request.json
    if result["status"] == "success":
        tokens = {
            'acess_token': create_access_token(identity=req_body["phone_number"]),
            'refresh_token': create_refresh_token(identity=req_body["phone_number"])
        }
        returns["status"] = result["status"]
        returns["result"] = tokens
        response_wrapper = Response(json.dumps(returns))
        response_wrapper.headers['Content-Type'] = 'application/json'
        return response_wrapper

    returns["message"] = result["message"]
    response_wrapper = Response(json.dumps(returns))
    response_wrapper.headers['Content-Type'] = 'application/json'
    return response_wrapper

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.users.find_one({"phone_number":identity})

@app.route('/topup', methods = ['POST'])
@jwt_required()
def topup():
    handler = Topup(db)

    result = handler.topup(current_user)

    returns = {}
    returns["status"] = "success"
    returns["result"] = result

    response_wrapper = Response(dumps(returns))
    response_wrapper.headers['Content-Type'] = 'application/json'
    return response_wrapper


@app.route('/pay', methods = ['POST'])
@jwt_required()
def payment():
    handler = Payment(db)

    result = handler.payment(current_user)

    returns = {}
    if "message" in result:
        returns["message"] = result["message"]
        response_wrapper = Response(dumps(returns))
        response_wrapper.headers['Content-Type'] = 'application/json'
        return response_wrapper

    returns["status"] = "success"
    returns["result"] = result

    response_wrapper = Response(dumps(returns))
    response_wrapper.headers['Content-Type'] = 'application/json'
    return response_wrapper

@app.route('/transfer', methods = ['POST'])
@jwt_required()
def transfer():
    handler = Transfer(db)

    result = handler.transfer(current_user)

    returns = {}
    if "message" in result:
        returns["message"] = result["message"]
        response_wrapper = Response(dumps(returns))
        response_wrapper.headers['Content-Type'] = 'application/json'
        return response_wrapper

    returns["status"] = "success"
    returns["result"] = result

    response_wrapper = Response(dumps(returns))
    response_wrapper.headers['Content-Type'] = 'application/json'
    return response_wrapper
 
@app.route('/transactions', methods = ['GET'])
@jwt_required()
def transactions():
    handler = Transaction(db)

    result = handler.transaction(current_user)

    returns = {}
    if "message" in result:
        returns["message"] = result["message"]
        response_wrapper = Response(dumps(returns))
        response_wrapper.headers['Content-Type'] = 'application/json'
        return response_wrapper

    returns["status"] = "success"
    returns["result"] = result

    response_wrapper = Response(dumps(returns))
    response_wrapper.headers['Content-Type'] = 'application/json'
    return response_wrapper

@app.route('/profile', methods = ['PUT'])
@jwt_required()
def profile():
    handler = Profile(db)

    result = handler.profile(current_user)

    returns = {}

    returns["status"] = "success"
    returns["result"] = result

    response_wrapper = Response(dumps(returns))
    response_wrapper.headers['Content-Type'] = 'application/json'
    return response_wrapper

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
