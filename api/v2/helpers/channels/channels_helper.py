from api.v2.models.channels.channels_model import Channels as ChannelsModel
from api.v2.models.channels.channels_schema import ChannelsSchema


def query_all_channels():
    all_channels = ChannelsModel.query.filter_by(state='active').all()
    channels = 'No channels found'
    if all_channels:
        channels = ChannelsSchema(many=True).dump(all_channels)

    return channels


def get_channels(bouquet_id):
    channels = ChannelsModel.query.filter_by(bouquet_id=bouquet_id).all()
    if channels:
        return ChannelsSchema(many=True).dump(channels)

    return None
