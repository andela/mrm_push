from api.v2.models.bouquets.bouquets_model import Bouquets as BouquetsModel
from api.v2.models.bouquets.bouquets_schema import BouquetsSchema


def query_all_bouquets():
    all_bouquets = BouquetsModel.query.filter_by(state='active').all()
    bouquets = 'No bouquets found'
    if all_bouquets:
        bouquets = BouquetsSchema(many=True).dump(all_bouquets)

    return bouquets


def create_bouquet(request_data):
    """Function to add bouquet to database
        :param request_data Required
            Post data sent to server
    """
    BouquetsModel.add_bouquet(bouquet_name=request_data['bouquet_name'], refresh_url=request_data['refresh_url'],
                              should_refresh=request_data['should_refresh'],
                              auth_credentials=request_data['auth_credentials'],
                              api_key1=request_data['api_key1'], api_key2=request_data['api_key2'])
    return {'message': 'successfully added bouquet', 'bouquet': request_data}
