from flask import Response, request, url_for
from flask_restful import Resource
from gamescoresapi import db
from gamescoresapi.models import Person, Game, Match
from gamescoresapi.constants import *
from gamescoresapi.utils import GamescoresBuilder, create_error_response

class GameCollection(Resource):

    def get():

    def post():

class GameItem(Resource):

    def get():

    def post():

    def put():

    def delete():