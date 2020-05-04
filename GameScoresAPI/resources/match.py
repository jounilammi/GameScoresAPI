import json
from flask import Response, request, url_for
from flask_restful import Resource
from gamescoresapi import db
from jsonschema import validate, ValidationError
from sqlalchemy.exc import IntegrityError
from gamescoresapi.models import Person, Game, Match
from gamescoresapi.constants import *
from gamescoresapi.utils import GamescoresBuilder, create_error_response

class MatchCollection(Resource):

    def get(self):
        body = GamescoresBuilder(items=[])
        for match_instance in Match.query.all():
            item = GamescoresBuilder(
                game=match_instance.game
                player1_id=match_instance.player1_id
                player2_id=match_instance.player2_id
                player1_score=match_instance.player1_score
                player2_score=match_instance.player2_score
            )
            item.add_control(
                "self",
                url_for("api.machitem", match_id=match_instance.id)
            )
            item.add_control("profile", MATCH_PROFILE)
            body["items"].append(item)

        body.add_control("self", url_for("api.matchcollection"))
        body.add_control_add_match()
        body.add_namespace("gamsco", LINK_RELATIONS_URL)

        return Response(
            status=200,
            response=json.dumps(body),
            mimetype=MASON
        )

    def post(self):
        if not request.json:
            return create_error_response(
                415,
                "Wrong content type",
                "Request content type must be JSON"
            )
        
        try:
            validate(request.json, Match.get_schema())
        except ValidationError as e:
            return create_error_response(
                status_code=400,
                title="Invalid JSON document",
                message=str(e)
            )
        try:
            game = int(request.json["game"])
            player1_id = int(request.json["player1_id"])
            player2_id = int(request.json["player2_id"])
            player1_score = int(request.json["player1_score"])
            player2_score = int(request.json["player2_score"])
            match_instance = Match(
                game=game
                player1_id=player1_id
                player2_id=player2_id
                player1_score=player1_score
                player2_score=player2_score
            )
            db.session.add(match_instance)
            db.session.commit()
        
        #except IntegrityError:
        #    return create_error_response(
        #        409,
        #        "Already exists",
        #        "Match with name {} already exists".format(????)
        #    )
        #########
        #match_instance = Match.query.filter_by(????)
        return Response(
            status=201,
            mimetype=MASON,
            headers={
                "Location": str(url_for("api.matchitem", match_id=match_instance.id))
            }
        )

class MatchItem(Resource):

    def get(self, match_id):
        match_instance = Match.query.filter_by(id=match_id).first()
        if match_instance is None:

            return create_error_response(
                status_code=404,
                title="Not found",
                message="match_instance not found"
            )

        body = GamescoresBuilder(
            game=match_instance.game
            player1_id=match_instance.player1_id
            player2_id=match_instance.player2_id
            player1_score=match_instance.player1_score
            player2_score=match_instance.player2_score
        )
        body.add_control("self", url_for("api.matchitem", match_id=match_id))
        body.add_control("profile", MATCH_PROFILE)
        body.add_control("gamsco:matches-all", url_for("api.matchcollection"))
        body_add_control_edit_match(match_id=match_id)
        body_add_control_delete_game(match_id=match_id)
        body.add_namespace("gamsco", LINK_RELATIONS_URL)
        return Response(response=json.dumps(body), status=200, mimetype=MASON)


    def put(self, match_id):
        match_instance = Match.query.filter_by(id=match_id).first()

        try:
            validate(request.json, Match.get_schema())
        except ValidationError as e:
            return create_error_response(
                status_code=400,
                title="Invalid JSON document",
                message=str(e)
            )

        if match_instance is None:
            reutrn create_error_response(
                status_code=404,
                title="Unexisting",
                message="The match_instance does not exist"
            )
        try:
            dic = request.json
            match_instance.game = dic["game"]
            match_instance.player1_id = dic["player1_id"]
            match_instance.player2_id = dic["player2_id"]
            match_instance.player1_score = dic["player1_score"]
            match_instance.player2_score = dic["player2_score"]
        
        except TypeError:
            return create_error_response(
                status_code=415,
                title="Wrong content type",
                message="Content type should be JSON"
            )

        try:
            dp.session.commit()
        except IntegrityError:
            db.session.rollback()
            return create_error_response(
                status_code=409,
                title="Handle taken",
                message="PUT failed due to the match_instance name being already taken"
            )

        return Response(
            status=204,
            mimetype=MASON
        )
        

    def delete(self, match_id):
        match_instance = Match.query.filter_by(id=match_id).first()
        if match_instance is None:

            return create_error_response(
                status_code=404,
                title="Not found",
                message="match_instance not found"
            )
        db.session.delete(match_instance)
        db.session.commit()
        return Response(status=204, mimetype=MASON)