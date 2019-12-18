from api.v2.models.channels.channels_model import Channels as ChannelsModel
from api.v2.models.channels.channels_schema import ChannelsSchema


def query_all_channels():
    all_channels = ChannelsModel.query.filter_by(state='active').all()
    channels = 'No channels found'
    if all_channels:
        channels = ChannelsSchema(many=True).dump(all_channels)

    return channels

def query_channel(resource_id):
    channel = ChannelsModel.query.filter_by(resource_id=resource_id).first()
    if channel:
        return ChannelsSchema(many=False).dump(channel)
    
    return None
