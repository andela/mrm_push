from flask_restful import Api
from flask import Blueprint

from api.v2.controllers.channels.channels_controller import Channels
from api.v2.controllers.boquets.bouquets_controller import (
    Bouquets, RefreshChannels)


api_v2 = Blueprint('mrmpush_2', __name__, url_prefix="/v2")

mrm_push = Api(api_v2)


"""Add mrm push resources"""

mrm_push.add_resource(Channels, '/channels', strict_slashes=False)
mrm_push.add_resource(Bouquets, '/bouquets', strict_slashes=False)
mrm_push.add_resource(
    RefreshChannels, '/refresh/<string:api_type>/<int:bouquet_id>',
    strict_slashes=False)
