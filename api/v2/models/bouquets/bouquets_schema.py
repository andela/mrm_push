from ma import ma

from api.v2.models.bouquets.bouquets_model import Bouquets as BouquetsModel


class BouquetsSchema(ma.Schema):
    class Meta:
        model = BouquetsModel
        fields = ('id', 'client_id', 'client_secret',  'auth_uri', 'token_uri',
                  'bouquet_name', 'should_refresh', 'refresh_url')
