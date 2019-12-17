from api.v2.models.bouquets.bouquets_model import Bouquets as BouquetsModel
from api.v2.models.bouquets.bouquets_schema import BouquetsSchema


def query_all_bouquets():
    all_bouquets = BouquetsModel.query.filter_by(state='active').all()
    bouquets = 'No bouquets found'
    if all_bouquets:
        bouquets = BouquetsSchema(many=True).dump(all_bouquets)

    return bouquets


def query_bouquet(bouquet_id):
    bouquet = BouquetsModel.query.filter_by(id=bouquet_id).first()
    if bouquet:
        return BouquetsSchema(many=False).dump(bouquet)
    return None
