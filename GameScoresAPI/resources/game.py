import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from gamescoresapi import db
from sqlalchemy.exc import IntegrityError
from gamescoresapi.models import Game
from gamescoresapi.constants import *
from gamescoresapi.utils import GamescoresBuilder, create_error_response

"""
Source and help received to game.py from
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/resource_test.py
and
https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/
"""

class GameCollection(Resource):

    def get(self):
        body = GamescoresBuilder(items=[])
        for game_instance in Game.query.all():
            item = GamescoresBuilder(
                name=game_instance.name,
                score_type=game_instance.score_type,
            )
            item.add_control(
                "self",
                url_for("api.gameitem", game_id=game_instance.id)
            )
            item.add_control("profile", GAME_PROFILE)
            body["items"].append(item)

        body.add_control("self", url_for("api.gamecollection"))
        body.add_control_add_game()
        body.add_namespace("gamsco", LINK_RELATIONS_URL)


        # Returns list of all games (GET)

        return Response(
            status=200,
            response=json.dumps(body),
            mimetype=MASON
        )

    def post(self):
        if not request.json:

            # Content did not use the proper content type, or the request body was not valid JSON.

            return create_error_response(
                    415,
                    "Wrong content type",
                    "Request content type must be JSON"
                )

        # The client is trying to send a JSON document that doesn't validate against the schema, or has invalid data.

        try:
            validate(request.json, Game.get_schema())
        except ValidationError as e:
            return create_error_response(
                status_code=400,
                title="Invalid JSON document",
                message=str(e)
            )

        try:
            name = str(request.json["name"])
            score_type = int(request.json["score_type"])
            game_instance = Game(
                name=name,
                score_type=score_type
            )
            db.session.add(game_instance)
            db.session.commit()

        # If a game with a existing name is added response 409 "Game  with that name already exists

        except IntegrityError:
            return create_error_response(
                409,
                "Already exists",
                "Game with name {} already exists".format(name)
            )
        game_instance = Game.query.filter_by(name=name).first()


        # Returns response of game instance (POST)

        return Response(
            status=201,
            mimetype=MASON,
            headers={
                "Location": str(url_for("api.gameitem", game_id=game_instance.id))
            }
        )


class GameItem(Resource):

    def get(self, game_id):
        game_instance = Game.query.filter_by(id=game_id).first()
        if game_instance is None:

            # The client is trying to send a JSON document that doesn't validate against the schema, or has is missing score_type.

            return create_error_response(
                status_code=404,
                title="Not found",
                message="game_instance not found"
            )

        body = GamescoresBuilder(
            name=game_instance.name,
            score_type=game_instance.score_type,
        )
        body.add_control("self", url_for("api.gameitem", game_id=game_id))
        body.add_control("profile", GAME_PROFILE)
        body.add_control("gamsco:games-all", url_for("api.gamecollection"))
        body.add_control_edit_game(game_id=game_id)
        body.add_control_delete_game(game_id=game_id)
        body.add_namespace("gamsco", LINK_RELATIONS_URL)

        # Returns the game representation

        return Response(response=json.dumps(body), status=200, mimetype=MASON)

    def put(self, game_id):
        game_instance = Game.query.filter_by(id=game_id).first()


        # The client is trying to send a JSON document that doesn't validate against the schema, or has non-existent release date.

        try:
            validate(request.json, Game.get_schema())
        except ValidationError as e:
            return create_error_response(
                status_code=400,
                title="Invalid JSON document",
                message=str(e)
            )

        if game_instance is None:

            # The client is trying to send a JSON document that doesn't validate against the schema, or has is missing score_type.

            return create_error_response(
                status_code=404,
                title="Unexisting",
                message="The game_instance does not exist"
            )
        try:
            dic = request.json
            game_instance.name = dic["name"]
            game_instance.score_type = dic["score_type"]

        # The client sent a request with the wrong content type or the request body was not valid JSON.

        except TypeError:
            return create_error_response(
                status_code=415,
                title="Wrong content type",
                message="Content type should be JSON"
            )


        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

            # If a game with a existing game_instance is added response 409 is raised

            return create_error_response(
                status_code=409,
                title="Handle taken",
                message="PUT failed due to the  game_instance name being already taken"
            )


        # Replace the game's representation with a new one. Missing optional fields will be set to null.

        return Response(
            status=204,
            mimetype=MASON
        )

    def delete(self, game_id):
        game_instance = Game.query.filter_by(id=game_id).first()
        if game_instance is None:

            # The client is trying to send a JSON document that doesn't validate against the schema, or has is missing score_type.

            return create_error_response(
                status_code=404,
                title="Not found",
                message="game_instance not found"
            )
        db.session.delete(game_instance)
        db.session.commit()

       # Delete game

        return Response(status=204, mimetype=MASON)