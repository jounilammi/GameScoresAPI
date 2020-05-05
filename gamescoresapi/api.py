from flask import Blueprint
from flask_restful import Api

from .resources.game import GameCollection, GameItem
from .resources.match import MatchCollection, MatchItem
from .resources.person import PersonCollection, PersonItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(GameCollection, "/games/")
api.add_resource(GameItem, "/games/<game_id>/")
api.add_resource(MatchCollection, "/games/<game_id>/matches/")
api.add_resource(MatchItem, "/games/<game_id>/matches/<match_id>/")
api.add_resource(PersonCollection, "/persons/")
api.add_resource(PersonItem, "/persons/<person_id>/")





