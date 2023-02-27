from flask import request, Response
from bson.json_util import dumps
import uuid
import json
from datetime import datetime, timedelta, date

class Payment:
    def __init__(self, db):
        self.db = db
        self.users = db.users

    def payment(self, user):
        req = request.json
        del user["_id"]
        balance_before = user["balance"]
    
        if int(balance_before) < req["amount"]:
            return {
                "message": "balance is not enough"
            }

        balance_after = int(balance_before - int(req["amount"]))
        payments = {
            "payment_id": str(uuid.uuid4()),
            "amount": int(req["amount"]),
            "remarks": req["remarks"],
            "balance_before": balance_before,
            "balance_after": balance_after,
            "created_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "user": user
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

        self.db.payments.insert_one(payments)
        del payments["_id"]

        return payments

