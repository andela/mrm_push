from helpers.database import db


def update_calendar(calendar, calendar_key, room):
        if not room['firebaseToken']:
            room['firebaseToken'] = ''
        if not calendar:
            key = len(db.keys('*Calendar*')) + 1
            calendar_key = 'Calendar:' + str(key)
        elif 'firebase_token' not in calendar.keys() or calendar['firebase_token'] == room['firebaseToken']:
            return None

        db.hmset(calendar_key, {'calendar_id': room['calendarId'], 'firebase_token': room['firebaseToken']})
        db.persist(calendar_key)