from flask import request, Response
from bson.json_util import dumps
import uuid
import json
from datetime import datetime, timedelta, date

class Transaction:
    def __init__(self, db):
        self.db = db
        self.users = db.users

    def transaction(self, user):
        top_ups = self.db.top_ups.find({"user.user_id": user["user_id"]})
        payments = self.db.payments.find({"user.user_id": user["user_id"]})
        transfers = self.db.transfers.find({"user_from.user_id": user["user_id"]})

        return {
            'topups': top_ups,
            'payments': payments,
            'transfers': transfers
        }
