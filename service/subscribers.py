
import json
from helpers.database import db
from flask import jsonify, render_template


class Subscriber():
    def subscribers(self):
        subscribers = []
        for key in db.keys('*Subscriber*'):
            subscriber = db.hgetall(key)
            if 'calendars' in subscriber.keys():
                subscriber.pop('calendars')
            subscribers.append(subscriber)
        return render_template(
            'subscribers.html',
            result=subscribers
        )

    def delete_subscribers(self, subscriber_key):
        for key in db.keys('*Subscriber*'):
            subscribers = db.hgetall(key) 
            if subscribers['subscriber_key'] == subscriber_key:
                db.delete(key)
                return jsonify({"message": "deleted"})
            else:
                return jsonify({"message": "This subscriber doesn't exist"})

    def edit_subscribers(self, subscriber_info, subscriber_key):
        def convert_to_dict(obj):
            new_object = {}
            for key, val in obj.items():
                if isinstance(val, dict):
                    new_object[key] = json.dumps(val)
                else:
                    new_object[key] = val
            return new_object

        for key in db.keys('*Subscriber*'):
            subscribers = db.hgetall(key)
            if subscribers['subscriber_key'] == subscriber_key:
                value = convert_to_dict(subscriber_info)
                db.hmset(key, value)
                return json.dumps(subscriber_info)
