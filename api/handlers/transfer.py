from flask import request, Response
from bson.json_util import dumps
import uuid
import json
from datetime import datetime, timedelta, date

class Transfer:
    def __init__(self, db):
        self.db = db
        self.users = db.users

    def transfer(self, user):
        req = request.json
        user_target = self.db.users.find_one({'user_id':req["target_user"]})

        if user_target is None:
            return {
                "message": "target user not found"
            }

        del user["_id"]
        del user_target["_id"]
        balance_before_from = user["balance"]
        balance_before_target = user_target["balance"]
    
        if int(balance_before_from) < req["amount"]:
            return {
                "message": "balance is not enough"
            }

        balance_after_from = int(balance_before_from - int(req["amount"]))
        balance_after_target = int(balance_before_target + int(req["amount"]))

        transfers = {
            "transfer_id": str(uuid.uuid4()),
            "amount": int(req["amount"]),
            "remarks": req["remarks"],
            "balance_before": balance_before_from,
            "balance_after": balance_after_from,
            "created_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        new_balance_from = {
            "$set": {
                "balance": balance_after_from
            }
        }

        new_balance_target = {
            "$set": {
                "balance": balance_after_target
            }
        }

        self.users.update_one(user, new_balance_from)
        self.users.update_one(user_target, new_balance_target)

        updated_user_from = self.users.find_one({"phone_number": user["phone_number"]})
        updated_user_target = self.users.find_one({"phone_number": user_target["phone_number"]})
        del updated_user_from["_id"]
        del updated_user_from["pin"]

        del updated_user_target["_id"]
        del updated_user_target["pin"]
        transfers["user_from"] = updated_user_from
        transfers["user_target"] = updated_user_target
        self.db.transfers.insert_one(transfers)
        del transfers["_id"]

        return transfers

