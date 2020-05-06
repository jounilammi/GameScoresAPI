import json
import datetime
from flask import Response, request, url_for
from flask_restful import Resource
from .. import db
from ..models import Person, Game, Match
from ..constants import *
from ..utils import GamescoresBuilder, create_error_response
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError


"""
Source and help received to person.py from
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/resource_test.py
and
https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/
"""


class PersonCollection(Resource):

    # https://gamescoresapi1.docs.apiary.io/#reference/person/persons/list-all-persons
    def get(self):
        body = GamescoresBuilder(items=[])
        for person_instance in Person.query.all():
            item = GamescoresBuilder(
                id=person_instance.id,
                username=person_instance.username,
                first_name=person_instance.first_name,
                last_name=person_instance.last_name,
                birthdate=str(person_instance.birthdate),
                description=person_instance.description
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

    # https://gamescoresapi1.docs.apiary.io/#reference/person/persons/add-person-information
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
            description = request.json.get("description", "")

            person_instance = Person(
                username=username,
                first_name=first_name,
                last_name=last_name,
                description=description

            )

            time_parts = request.json.get("birthdate", "")
            if time_parts:
                time_parts = time_parts.split("-")
                try:
                    person_instance.birthdate = datetime.datetime(
                        year=int(time_parts[0]),
                        month=int(time_parts[1]),
                        day=int(time_parts[2]),
                    )
                except Exception:
                    pass

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

    # https://gamescoresapi1.docs.apiary.io/#reference/person/person/person-information
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
            id=person_instance.id,
            username=person_instance.username,
            first_name=person_instance.first_name,
            last_name=person_instance.last_name,
            birthdate=str(person_instance.birthdate),
            description=person_instance.description
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

    # https://gamescoresapi1.docs.apiary.io/#reference/person/person/edit-person
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
            person_instance.last_name = dic["last_name"]
            person_instance.description = dic.get("description", "")
            time_parts = dic.get("birthdate", "")
            if time_parts:
                time_parts = time_parts.split("-")
                try:
                    person_instance.birthdate = datetime.datetime(
                        year=int(time_parts[0]),
                        month=int(time_parts[1]),
                        day=int(time_parts[2]),
                    )
                except Exception:
                    pass

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

    # https://gamescoresapi1.docs.apiary.io/#reference/person/person/delete-person
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