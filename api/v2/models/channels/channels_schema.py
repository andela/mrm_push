from ma import ma
from api.v2.models.channels.channels_model import Channels as ChannelsModel


class ChannelsSchema(ma.Schema):
    class Meta:
        model = ChannelsModel
        fields = ("id", "channel_id", "calendar_id",
                  "resource_id", "extra_atrributes", "bouquet_id")
