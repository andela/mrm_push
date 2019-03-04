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
