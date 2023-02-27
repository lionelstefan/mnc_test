from flask import request, Response
from bson.json_util import dumps
import uuid
import json
from datetime import datetime, timedelta, date

class Topup:
    def __init__(self, db):
        self.db = db
        self.users = db.users

    def topup(self, user):
        req = request.json
        del user["_id"]
        balance_before = user["balance"]
        balance_after = int(balance_before + int(req["amount"]))
        topups = {
            "top_up_id": str(uuid.uuid4()),
            "amount_top_up": int(req["amount"]),
            "balance_before": balance_before,
            "balance_after": balance_after,
            "created_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        new_balance = {
            "$set": {
                "balance": balance_after
            }
        }

        self.users.update_one(user, new_balance)

        updated_user = self.users.find_one({"phone_number": user["phone_number"]})
        del updated_user["_id"]
        del updated_user["pin"]
        topups["user"] = updated_user
        self.db.top_ups.insert_one(topups)

        del topups["_id"]
        return topups

