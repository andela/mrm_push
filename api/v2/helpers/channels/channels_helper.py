from api.v2.models.channels.channels_model import Channels as ChannelsModel
from api.v2.models.channels.channels_shema import ChannelsSchema


def query_all_channels():
    all_channels = ChannelsModel.query.filter_by(state='active').all()
    channels = 'No channels found'
    if all_channels:
        channels = ChannelsSchema(many=True).dump(all_channels)

    return channels


def query_channel(channel_id):
    channel = ChannelsModel.query.filter_by(
        state='active', id=channel_id).first()

    return channel


def query_bouquet_channels(bouquet_id):
    all_channels = ChannelsModel.query.filter_by(
        state='active', bouquet_id=bouquet_id).all()
    bouquet_channels = {}
    if all_channels:
        bouquet_channels = ChannelsSchema(many=True).dump(all_channels)

    return bouquet_channels
