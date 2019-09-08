import requests
from api.v2.models.bouquets.bouquets_model import Bouquets as BouquetsModel
from api.v2.models.channels.channels_model import Channels as ChannelsModel
from api.v2.models.bouquets.bouquets_schema import BouquetsSchema
from api.v2.helpers.channels.channels_helper import (
    query_bouquet_channels, query_channel)


def query_all_bouquets():
    all_bouquets = BouquetsModel.query.filter_by(state='active').all()
    bouquets = 'No bouquets found'
    if all_bouquets:
        bouquets = BouquetsSchema(many=True).dump(all_bouquets)

    return bouquets


def query_bouquet(bouquet_id):
    bouquet_query = BouquetsModel.query.filter_by(
        state='active', id=bouquet_id).first()
    bouquet = BouquetsSchema().dump(bouquet_query)
    return bouquet


def refresh_bouquet_channels(api_type, bouquet_id):
    """helper function for refreshing channels"""
    response = {'response': {'Error': 'Bouquet not found!'}, 'code': 404}
    bouquet = query_bouquet(bouquet_id)
    if bouquet:
        response = {'response':
                    {"Error": "Refresh endpoint not responding appropriatly"},
                    'code': 424
                    }
        bouquet_channels = fetch_bouquet_channels(
            api_type, bouquet['refresh_url'])
        if bouquet_channels:
            channel_update = update_channels(bouquet_id, bouquet_channels)
            response = {'response': {
                "Success": channel_update}, 'code': 200}

    return response


def fetch_bouquet_channels(api_type, refresh_url):
    if api_type == 'restful_api':
        return restful_channels(refresh_url)

    return graphql_channels(refresh_url)


def graphql_channels(refresh_url):
    """fetch channels from bouquets with grapghql endpoints"""
    channels_query = (
        {
            "query":
            "{ allChannels { channels { calendarId, firebaseToken } } }"
        })
    try:
        response = requests.get(url=refresh_url, json=channels_query)
        channels = response.json()['data']['allChannels']['channels']
    except Exception:
        channels = False
    return channels


def restful_channels(refresh_url):
    """fetch channels from bouquets with restful endpoints"""
    try:
        response = requests.get(refresh_url)
        channels = response.json()['channels']
    except Exception:
        channels = False
    return channels


def update_channels(bouquet_id, bouquet_channels):
    subscribed_channels = query_bouquet_channels(bouquet_id)
    for channel in bouquet_channels:
        existing_channel = filter(
            lambda subscribed_channel:
            subscribed_channel['calendar_id'] == channel['calendarId'],
            subscribed_channels)
        if not list(existing_channel):
            ChannelsModel(channel_id="", calendar_id=channel['calendarId'],
                          resource_id="",
                          extra_atrributes=channel['firebaseToken'],
                          bouquet_id=bouquet_id).save()

    for channel in subscribed_channels:
        db_channel = query_channel(channel['id'])
        existing_channel = filter(
            lambda bouquet_channel:
            bouquet_channel['calendarId'] == channel['calendar_id'],
            bouquet_channels)
        if not list(existing_channel):
            db_channel.state = 'deleted'
            db_channel.save()

    return 'Bouquet channels refreshed succesfully'
