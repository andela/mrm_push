from helpers.database import db_session
from apiclient import errors


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


def update_entity_fields(entity, **kwargs):
    """
    Function to update an entities fields
    :param kwargs
    :param entity
    """
    keys = kwargs.keys()
    for key in keys:
        exec("entity.{0} = kwargs['{0}']".format(key))
    return entity


class Utility(object):

    def save(self):
        """Function for saving new objects"""
        db_session.add(self)
        db_session.commit()
