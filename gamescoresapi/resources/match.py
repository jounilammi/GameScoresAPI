import json
import datetime
from flask import Response, request, url_for
from flask_restful import Resource
from .. import db
from jsonschema import validate, ValidationError
from sqlalchemy.exc import IntegrityError
from ..models import Person, Game, Match
from ..constants import *
from ..utils import GamescoresBuilder, create_error_response

"""
Source and help received to match.py from
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/resource_test.py
and
https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/
"""

class MatchCollection(Resource):


    # https://gamescoresapi1.docs.apiary.io/#reference/match/matches/list-all-matches
    def get(self, game_id):
        body = GamescoresBuilder(items=[])
        for match_instance in Match.query.filter_by(game=game_id):
            item = GamescoresBuilder(
                id=match_instance.id,
                game=match_instance.game,
                player1_id=match_instance.player1_id,
                player2_id=match_instance.player2_id,
                player1_score=match_instance.player1_score,
                player2_score=match_instance.player2_score,
                place=match_instance.place,
                time=str(match_instance.time),
                comment=match_instance.comment
            )
            item.add_control(
                "self",
                url_for(
                    "api.matchitem",
                    game_id=match_instance.game,
                    match_id=match_instance.id
                )
            )
            item.add_control("profile", MATCH_PROFILE)
            body["items"].append(item)

        body.add_control("self", url_for("api.matchcollection", game_id=game_id))
        body.add_control_add_match(game_id=game_id)
        body.add_namespace("gamsco", LINK_RELATIONS_URL)

        '''
        Returns list of all matches (GET)
        '''
        return Response(
            status=200,
            response=json.dumps(body),
            mimetype=MASON
        )

    # https://gamescoresapi1.docs.apiary.io/#reference/match/matches/add-match
    def post(self, game_id):
        if not request.json:
            '''
            Content did not use the proper content type, or the request body was not valid JSON.
            '''
            return create_error_response(
                415,
                "Wrong content type",
                "Request content type must be JSON"
            )
        '''
        The client is trying to send a JSON document that doesn't validate against the schema, or has invalid data.
        '''
        try:
            validate(request.json, Match.get_schema())

        except ValidationError as e:
            return create_error_response(
                status_code=400,
                title="Invalid JSON document",
                message=str(e)
            )

        game_id = int(request.json["game"])
        player1_id = int(request.json["player1_id"])
        player2_id = int(request.json["player2_id"])
        player1_score = int(request.json["player1_score"])
        player2_score = int(request.json["player2_score"])
        place = request.json.get("place", "")
        comment = request.json.get("comment", "")
        match_instance = Match(
            game=game_id,
            player1_id=player1_id,
            player2_id=player2_id,
            player1_score=player1_score,
            player2_score=player2_score,
            place=place,
            comment=comment
        )
        time_parts = request.json.get("time", "")
        if time_parts:
            time_parts = time_parts.split("-")
            try:
                match_instance.time = datetime.datetime(
                    year=int(time_parts[0]),
                    month=int(time_parts[1]),
                    day=int(time_parts[2]),
                    hour=int(time_parts[3]),
                    minute=int(time_parts[4]),
                )
            except Exception:
                pass

        db.session.add(match_instance)
        db.session.commit()

        '''
        Returns response of match_instance (POST)
        '''
        return Response(
            status=201,
            mimetype=MASON,
            headers={
                "Location": str(url_for("api.matchitem", game_id=game_id, match_id=match_instance.id))
            }
        )

class MatchItem(Resource):

    #https://gamescoresapi1.docs.apiary.io/#reference/match/match/match-information
    def get(self, game_id, match_id):
        match_instance = Match.query.filter_by(game=game_id).filter_by(id=match_id).first()
        if match_instance is None:

            '''
            The client is trying to send a JSON document that doesn't validate against the schema, or has is missing score_type.
            '''
            return create_error_response(
                status_code=404,
                title="Not found",
                message="match_instance not found"
            )

        body = GamescoresBuilder(
            id=match_instance.id,
            game=match_instance.game,
            player1_id=match_instance.player1_id,
            player2_id=match_instance.player2_id,
            player1_score=match_instance.player1_score,
            player2_score=match_instance.player2_score,
            place=match_instance.place,
            time=str(match_instance.time),
            comment=match_instance.comment
        )
        body.add_control("self", url_for("api.matchitem", game_id=game_id, match_id=match_id))
        body.add_control("profile", MATCH_PROFILE)
        body.add_control("gamsco:matches-all", url_for("api.matchcollection", game_id=game_id))
        body.add_control_edit_match(game_id=game_id, match_id=match_id)
        body.add_control_delete_match(game_id=game_id, match_id=match_id)
        body.add_namespace("gamsco", LINK_RELATIONS_URL)
        '''
        Returns the match representation
        '''
        return Response(response=json.dumps(body), status=200, mimetype=MASON)

    # https://gamescoresapi1.docs.apiary.io/#reference/match/match/edit-match
    def put(self, game_id, match_id):
        match_instance = Match.query.filter_by(game=game_id).filter_by(id=match_id).first()

        '''
        The client is trying to send a JSON document that doesn't validate against the schema, or has non-existent release date.
        '''
        try:
            validate(request.json, Match.get_schema())
        except ValidationError as e:
            return create_error_response(
                status_code=400,
                title="Invalid JSON document",
                message=str(e)
            )

        if match_instance is None:
            '''
            The client is trying to send a JSON document that doesn't validate against the schema, or has is missing score_type.
            '''
            return create_error_response(
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
            match_instance.place = dic.get("place", "")
            match_instance.comment = dic.get("comment", "")
            time_parts = dic.get("time", "")
            if time_parts:
                time_parts = time_parts.split("-")
                try:
                    match_instance.time = datetime.datetime(
                        year=int(time_parts[0]),
                        month=int(time_parts[1]),
                        day=int(time_parts[2]),
                        hour=int(time_parts[3]),
                        minute=int(time_parts[4])
                    )
                except Exception:
                    pass




            # The client sent a request with the wrong content type or the request body was not valid JSON.

        except TypeError:
            return create_error_response(
                status_code=415,
                title="Wrong content type",
                message="Content type should be JSON"
            )


        db.session.commit()

        '''
        Replace the matche's representation with a new one. Missing optional fields will be set to null.
        '''
        return Response(
            status=204,
            mimetype=MASON
        )

    # https://gamescoresapi1.docs.apiary.io/#reference/match/match/delete-match
    def delete(self, game_id, match_id):
        match_instance = Match.query.filter_by(game=game_id).filter_by(id=match_id).first()
        if match_instance is None:
            '''
            The client is trying to send a JSON document that doesn't validate against the schema.
            '''
            return create_error_response(
                status_code=404,
                title="Not found",
                message="match_instance not found"
            )
        db.session.delete(match_instance)
        db.session.commit()
        '''
        Delete match
        '''
        return Response(status=204, mimetype=MASON)