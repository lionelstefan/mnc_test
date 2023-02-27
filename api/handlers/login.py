from flask import request, Response
from bson.json_util import dumps
import json

class Login:
    def __init__(self, db):
        self.db = db
        self.users = db.users

    def login(self):
        req = request.json
        phone_number = req['phone_number']
        pin = req['pin']

        user = self.users.find_one({'phone_number': phone_number})

        response = {}
        if user is None:
            response["status"] = "failed"
            response["message"] = "user is not exist"
            return response

        if (user["pin"] != pin):
            response["status"] = "failed"
            response["message"] = "phone number and pin dont match"
            return response

        response["status"] = "success"
        return response

