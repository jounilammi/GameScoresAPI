import json

from flask import Response, request, url_for
from flask_restful import Resource
from gamescoresapi import db
from gamescoresapi.models import Person, Game, Match
from gamescoresapi.constants import *
from gamescoresapi.utils import GamescoresBuilder, create_error_response
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError



class PersonCollection(Resource):

    def get(self):
        body = GamescoresBuilder(items=[])
        for game_instance in Game.query.all():
            item = GamescoresBuilder(
                username=person_instance.username,
                first_name=person_instance.first_name,
                last_name=person_instance.last_name,
            )
            item.add_control(
                "self",
                url_for("api.personitem", person_id=person_instance.id)
            )
            item.add_control("profile", PERSON_PROFILE)
            body["items"].append(item)

        body.add_control("self", url_for("api.personcollection"))
        body.add_control_add_person()
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
            validate(request.json, Person.get_schema())
        except ValidationError as e:
            return create_error_response(
                status_code=400,
                title="Invalid JSON document",
                message=str(e)
            )
        try:
            username = str(request.json["username"])
            first_name = str(request.json["first_name"])
            last_name = str(request.json["last_name"])
            person_instance = Person(
                username=username,
                first_name=first_name
                last_name=last_name
            )
            db.session.add(person_instance)
            db.session.commit()
        except IntegrityError:
            return create_error_response(
                409,
                "Already exists",
                "Person with username {} already exists".format(username)
            )
        person_instance = Person.query.filter_by(username=username).first()
        return Response(
            status=201,
            mimetype=MASON,
            headers={
                "Location": str(url_for("api.personitem", person_id=person_instance.id))
            }
        )


class PersonItem(Resource):

    def get(self, person_id):
        person_instance = Person.query.filter_by(id=person_id).first()
        if person_instance is None:

            return create_error_response(
                status_code=404,
                title="Not found",
                message="person_instance not found"
            )

        body = GamescoresBuilder(
            username=person_instance.username,
            first_name=person_instance.first_name,
            last_name=person_instance.last_name,
        )
        body.add_control("self", url_for("api.personitem", person_id=person_id))
        body.add_control("profile", PERSON_PROFILE)
        body.add_control("gamsco:persons-all", url_for("api.personcollection"))
        body.add_control_edit_person(person_id=person_id)
        body.add_control_delete_person(person_id=person_id)
        body.add_namespace("gamsco", LINK_RELATIONS_URL)
        return Response(response=json.dumps(body), status=200, mimetype=MASON)

    def post(self, person_id):
        pass

    def put(self, person_id):
        person_instance = Person.query.filter_by(id=person_id).first()

        try:
            validate(request.json, Person.get_schema())
        except ValidationError as e:
            return create_error_response(
                status_code=400,
                title="Invalid JSON document",
                message=str(e)
            )

        if person_instance is None:
            return create_error_response(
                status_code=404,
                title="Unexisting",
                message="The person_instance does not exist"
            )
        try:
            dic = request.json
            person_instance.username = dic["username"]
            person_instance.first_name = dic["first_name"]
            person_instance.last_name = dic["score_type"]

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
            return create_error_response(
                status_code=409,
                title="Handle taken",
                message="PUT failed due to the  person_instance name being already taken"
            )

        return Response(
            status=204,
            mimetype=MASON
        )

    def delete(self, person_id):
        person_instance = Person.query.filter_by(id=person_id).first()
        if person_instance is None:

            return create_error_response(
                status_code=404,
                title="Not found",
                message="person_instance not found"
            )
        db.session.delete(person_instance)
        db.session.commit()
        return Response(status=204, mimetype=MASON)