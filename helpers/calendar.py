from helpers.database import db


def update_calendar(calendar, calendar_key, room):
        if not room['firebaseToken']:
            room['firebaseToken'] = ''
        if not calendar:
            key = len(db.keys('*Calendar*')) + 1
            db.hmset('Calendar:' + str(key), {'calendar_id': room['calendarId'], 'firebase_token': room['firebaseToken']})
        if 'firebase_token' in calendar.keys() and calendar['firebase_token'] != room['firebaseToken']:
            db.hmset(calendar_key, {'calendar_id': room['calendarId'], 'firebase_token': room['firebaseToken']})
