from flask import Blueprint
from flask_restful import Api

from gamescoresapi.resources.game import GameCollection, GameItem
from gamescoresapi.resources.match import MatchCollection, MatchItem
from gamescoresapi.resources.person import PersonCollection, PersonItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(GameCollection, "/games/")
api.add_resource(GameItem, "/games/<game>/")
api.add_resource(MatchCollection, "/games/<game_id>/matches/")
api.add_resource(MatchItem, "/games/<game_id>/matches/<match>/")
api.add_resource(PersonCollection, "/persons/")
api.add_resource(PersonItem, "/persons/<id>/")





