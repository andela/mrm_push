import datetime

from apiclient import errors
from ..helpers.database import db


def stop_channel(service, channel_id, resource_id):
    """
    Function to stop watching a specific channel.
    :param service - Calendar API service instance.
    :param channel_id - ID of the channel to stop.
    :param resource_id - Resource ID of the channel to stop.
    """
    body = {
        'id': channel_id,
        'resourceId': resource_id
    }
    try:
        return service.channels().stop(body=body).execute()
    except errors.HttpError as error:
        print('An error occurred', error)


def save_to_db(*args):
    """ Function to save to database."""
    results = (args)
    result = results[0]
    key = len(db.keys('*Notification*')) + 1
    result['time'] = datetime.datetime.now().replace(
                second=0, microsecond=0
            )
    notification_details = {'time': str(result['time']),
                            'results': str(result['results']),
                            'subscriber_info': str(result['subscriber_info']),
                            'platform': str(result['platform'])
                            }
    db.hmset('Notification:' + str(key), notification_details)
