import json

from flask import Response, request, url_for
from flask_restful import Resource
from gamescoresapi import db
from gamescoresapi.models import Person, Game, Match
from gamescoresapi.constants import *
from gamescoresapi.utils import GamescoresBuilder, create_error_response
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError


"""
Source and help received to game.py from
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/resource_test.py
and
https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/
"""


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

        '''
        Returns list of all persons (GET)
        '''
        return Response(
            status=200,
            response=json.dumps(body),
            mimetype=MASON
        )


    def post(self):
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
                first_name=first_name,
                last_name=last_name
            )
            db.session.add(person_instance)
            db.session.commit()
            '''
            If a person with a existing name is added response 409 "Game  with that name already exists"
            '''
        except IntegrityError:
            return create_error_response(
                409,
                "Already exists",
                "Person with username {} already exists".format(username)
            )
        person_instance = Person.query.filter_by(username=username).first()

        '''
        Returns response of person_instance (POST)
        '''
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


            '''
            The client is trying to send a JSON document that doesn't validate against the schema.
            '''
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
        '''
        Returns the person's representation
        '''
        return Response(response=json.dumps(body), status=200, mimetype=MASON)

    def post(self, person_id):
        pass

    def put(self, person_id):
        person_instance = Person.query.filter_by(id=person_id).first()

        '''
        The client is trying to send a JSON document that doesn't validate against the schema, or has non-existent release date.
        '''
        try:
            validate(request.json, Person.get_schema())
        except ValidationError as e:
            return create_error_response(
                status_code=400,
                title="Invalid JSON document",
                message=str(e)
            )

        if person_instance is None:
            '''
            The client is trying to send a JSON document that doesn't validate against the schema.
            '''
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

            '''
            The client sent a request with the wrong content type or the request body was not valid JSON.
            '''
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
            '''
            If a peson with a existing game_instance is added response 409 is raised
            '''
            return create_error_response(
                status_code=409,
                title="Handle taken",
                message="PUT failed due to the  person_instance name being already taken"
            )
        '''
        Replace the person's representation with a new one. Missing optional fields will be set to null.
        '''
        return Response(
            status=204,
            mimetype=MASON
        )

    def delete(self, person_id):
        person_instance = Person.query.filter_by(id=person_id).first()
        if person_instance is None:
            '''
            The client is trying to send a JSON document that doesn't validate against the schema.
            '''
            return create_error_response(
                status_code=404,
                title="Not found",
                message="person_instance not found"
            )
        db.session.delete(person_instance)
        db.session.commit()
        '''
        Delete peson
        '''
        return Response(status=204, mimetype=MASON)