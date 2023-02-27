from flask import request, Response
from bson.json_util import dumps
import uuid
import json
from datetime import datetime, timedelta, date

class Register:
    def __init__(self, db):
        self.db = db
        self.users = db.users

    def regist(self):
        req = request.json
        save = req
        save['user_id'] = str(uuid.uuid4())
        save['balance'] = 0
        save['created_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        key = {
            "phone_number": save["phone_number"]
        }
        response = {}
        check = self.users.find_one(key)
        if check is None:
            user = self.users.insert_one(save)
            del save["_id"]
            response["result"] = save
            response["status"] = "success"
            return json.dumps(response)

        response["message"] = "Phone Number already registered"
        return json.dumps(response)

