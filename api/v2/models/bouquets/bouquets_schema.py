from ma import ma
from api.v2.models.bouquets.bouquets_model import Bouquets as BouquetsModel


class BouquetsSchema(ma.Schema):
    class Meta:
        model = BouquetsModel
        fields = ("id", "bouquet_id", "api_key1",  "api_key2"
                  "auth_credentials", "bouquet_name", "should_refresh")
