from api.v2.models.channels.channels_model import Channels as ChannelsModel
from api.v2.models.channels.channels_shema import ChannelsSchema


def query_all_channels():
    all_channels = ChannelsModel.query.filter_by(state='active').all()
    channels = 'No channels found'
    if all_channels:
        channels = ChannelsSchema(many=True).dump(all_channels)

    return channels
