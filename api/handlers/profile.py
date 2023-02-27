from flask import request, Response
from bson.json_util import dumps
import uuid
import json
from datetime import datetime, timedelta, date

class Profile:
    def __init__(self, db):
        self.db = db
        self.users = db.users

    def profile(self, user):
        new_fields = request.json
        new_fields["updated_date"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_profile = {
            "$set": new_fields
        }

        del user["_id"]
        self.db.users.update_one(user, new_profile)
        updated = self.db.users.find_one({"user_id":user["user_id"]})

        return updated
