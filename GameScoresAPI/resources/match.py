from flask import Response, request, url_for
from flask_restful import Resource
from gamescoresapi import db
from gamescoresapi.models import Person, Game, Match
from gamescoresapi.constants import *
from gamescoresapi.utils import GamescoresBuilder, create_error_response

class MatchCollection(Resource):

    def get(self):
        pass

    def post(self):
        pass

class MatchItem(Resource):

    def get(self, id):
        pass

    def post(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass