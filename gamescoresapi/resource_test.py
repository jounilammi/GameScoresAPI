import json
import os
import pytest
import tempfile
import time

from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

from . import db, create_app
from .api import api
from .resources.game import GameCollection, GameItem
from .resources.match import MatchCollection, MatchItem
from .resources.person import PersonCollection, PersonItem
from .models import Game, Match, Person

from datetime import datetime

"""
Source and help received to resource_test.py from
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/resource_test.py
and
https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/
"""

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# based on http://flask.pocoo.org/docs/1.0/testing/
# we don't need a client for database testing, just the db handle
@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }

    app = create_app(config)

    with app.app_context():
        db.create_all()
        _populate_db()

    yield app.test_client()

    os.close(db_fd)
    os.unlink(db_fname)


def _get_person(word="a"):
    '''
    person = Person(username="NickName",
    first_name="Testy", last_name="Tester")
    '''
    return(Person(username=word, first_name="Testy", last_name="Tester"))


def _get_match(p1_id, p2_id, game_id):
    match = Match(
        game=game_id,
        player1_id=p1_id,
        player2_id=p2_id,
        player1_score=23,
        player2_score=30,
        comment="well played"
    )
    return(match)


def _get_game(gamename="a", score_type=1):
    game = Game(name=gamename, score_type=1)
    return(game)


def _populate_db():
    """
    Pre-populate database with 2 matches, 2 players and 2 matches
    """

    person1 = _get_person("aaaa")
    person2 = _get_person("bbbb")
    game = _get_game("football", score_type=1)
    game2 = _get_game("golf", score_type=2)
    match = _get_match(p1_id=1, p2_id=2, game_id=1)
    match2 = _get_match(p1_id=1, p2_id=2, game_id=2)

    db.session.add(person1)
    db.session.add(person2)
    db.session.add(game)
    db.session.add(game2)
    db.session.add(match)
    db.session.add(match2)

    db.session.commit()


def _check_namespace(client, response):
    """
    Checks that the "gamsco" namespace is found from the response body, and
    that its "name" attribute is a URL that can be accessed.
    """

    ns_href = response["@namespaces"]["gamsco"]["name"]
    resp = client.get(ns_href)
    assert resp.status_code == 200


def _check_control_get_method(ctrl, client, obj):
    """
    Checks a GET type control from a JSON object be it root document or an item
    in a collection. Also checks that the URL of the control can be accessed.
    """

    href = obj["@controls"][ctrl]["href"]
    resp = client.get(href)
    assert resp.status_code == 200


def _check_control_delete_method(ctrl, client, obj):
    """
    Checks a DELETE type control from a JSON object be it root document or an
    item in a collection. Checks the contrl's method in addition to its "href".
    Also checks that using the control results in the correct status code of 204.
    """

    href = obj["@controls"][ctrl]["href"]
    method = obj["@controls"][ctrl]["method"].lower()
    assert method == "delete"
    resp = client.delete(href)
    assert resp.status_code == 204


def _check_control_put_method_for_person(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid game against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """

    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_person_json()
    body["username"] = obj["username"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204


def _check_control_put_method_for_match(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid game against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """

    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_match_json()
    body["player1_id"] = obj["player1_id"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204


def _check_control_put_method_for_game(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid game against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """

    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_game_json()
    body["name"] = obj["name"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204


def _check_control_post_method_for_person(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid game against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """

    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_person_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

def _check_control_post_method_for_match(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid game against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """

    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_match_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

def _check_control_post_method_for_game(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid game against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """

    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_game_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

def _get_game_json(number=1):
    """
    Creates a valid game JSON object to be used for PUT and POST tests.
    """

    return {"id": 1, "name": "Tennis", "score_type": 1}


def _get_match_json(number=1):
    """
    Creates a valid game JSON object to be used for PUT and POST tests.
    """

    return {"id": 1, "game": 1, "player1_id": 1, "player2_id": 2, "player1_score": 13, "player2_score": 16}


def _get_person_json(number=1):
    """
    Creates a valid game JSON object to be used for PUT and POST tests.
    """
    return {"id": 1, "username": "mattdamon", "first_name": "Matt", "last_name": "Damon"}


class TestGameCollection(object):

    RESOURCE_URL = "/api/games/"

    def test_get(self, client):
        """
        Checks a GET type control from a JSON object be it root document or an item
        in a collection. Also checks that the URL of the control can be accessed.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_post_method_for_game("gamsco:add-game", client, body)
        assert len(body["items"]) == 2
        for item in body["items"]:
            _check_control_get_method("self", client, item)
            _check_control_get_method("profile", client, item)

    def test_post(self, client):
        """
        Checks a POST type test from a JSON object be it root document or an item
        in a collection. Checks that using the control results in the correct
        status code of 201. Tests the content type and validates that it exist.
        """


        valid = _get_game_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        # assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["id"] + "/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # remove model field for 400
        valid.pop("name")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestGameItem(object):

    RESOURCE_URL = "/api/games/1/"
    INVALID_URL = "/api/games/23341/"

    def test_get(self, client):
        """
        Checks a GET type control from a JSON object be it root document or an item
        in a collection. Also checks that the URL of the control can be accessed.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("gamsco:games-all", client, body)
        _check_control_put_method_for_game("edit", client, body)
        _check_control_delete_method("gamsco:delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Checks a PUT type control from a JSON object be it root document or an item
        in a collection. In addition to checking the "href" attribute, also checks
        that method, encoding and schema can be found from the control. Also
        validates a valid game against the schema of the control to ensure that
        they match. Finally checks that using the control results in the correct
        status code of 204.
        """

        valid = _get_game_json()
        valid.pop("id")
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another game's name
        valid["name"] = "golf"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # test with valid (only change model)
        valid = _get_game_json()
        valid.pop("id")
        valid["score_type"] = 2
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove field for 400
        valid.pop("score_type")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        """
        Checks a DELETE type control from a JSON object be it root document or an
        item in a collection. Checks the contrl's method in addition to its "href".
        Also checks that using the control results in the correct status code of 204.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404


class TestMatchCollection(object):

    RESOURCE_URL = "/api/games/1/matches/"

    def test_get(self, client):
        """
        Checks a GET type control from a JSON object be it root document or an item
        in a collection. Also checks that the URL of the control can be accessed.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_post_method_for_match("gamsco:add-match", client, body)
        assert len(body["items"]) == 2
        for item in body["items"]:
            _check_control_get_method("self", client, item)
            _check_control_get_method("profile", client, item)

    def test_post(self, client):
        """
        Checks a POST type test from a JSON object be it root document or an item
        in a collection. Checks that using the control results in the correct
        status code of 201. Tests the content type and validates that it exist.
        """

        valid = _get_match_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        # assert resp.headers["Location"].endswith(
        #     self.RESOURCE_URL + str(valid["id"]) + "/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200

        # remove model field for 400
        valid.pop("player1_id")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestMatchItem(object):

    RESOURCE_URL = "/api/games/1/matches/1/"
    INVALID_URL = "/api/games/1/matches/aa/"

    def test_get(self, client):
        """
        Checks a GET type control from a JSON object be it root document or an item
        in a collection. Also checks that the URL of the control can be accessed.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("gamsco:matches-all", client, body)
        _check_control_put_method_for_match("edit", client, body)
        _check_control_delete_method("gamsco:delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Checks a PUT type control from a JSON object be it root document or an item
        in a collection. In addition to checking the "href" attribute, also checks
        that method, encoding and schema can be found from the control. Also
        validates a valid game against the schema of the control to ensure that
        they match. Finally checks that using the control results in the correct
        status code of 204.
        """

        valid = _get_match_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another matche's name
        valid["game"] = 5
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # test with valid (only change model)
        valid["game"] = 1
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove field for 400
        valid.pop("model")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        """
        Checks a DELETE type control from a JSON object be it root document or an
        item in a collection. Checks the contrl's method in addition to its "href".
        Also checks that using the control results in the correct status code of 204.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404


class TestPersonCollection(object):

    RESOURCE_URL = "/api/persons/"

    def test_get(self, client):
        """
        Checks a GET type control from a JSON object be it root document or an item
        in a collection. Also checks that the URL of the control can be accessed.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_post_method_for_person("gamsco:add-person", client, body)
        assert len(body["items"]) == 2
        for item in body["items"]:
            _check_control_get_method("self", client, item)
            _check_control_get_method("profile", client, item)

    def test_post(self, client):
        """
        Checks a POST type test from a JSON object be it root document or an item
        in a collection. Checks that using the control results in the correct
        status code of 201. Tests the content type and validates that it exist.
        """

        valid = _get_person_json()

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        # test with valid and see that it exists afterward
        pers_id = str(valid["id"])
        valid.pop("id")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

        # assert resp.headers["Location"].endswith(self.RESOURCE_URL + pers_id + "/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # remove model field for 400
        valid.pop("username")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestPersonItem(object):

    RESOURCE_URL = "/api/persons/1/"
    INVALID_URL = "/api/persons/23341/"

    def test_get(self, client):
        """
        Checks a GET type control from a JSON object be it root document or an item
        in a collection. Also checks that the URL of the control can be accessed.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("gamsco:persons-all", client, body)
        _check_control_put_method_for_person("edit", client, body)
        _check_control_delete_method("gamsco:delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        """
        Checks a PUT type control from a JSON object be it root document or an item
        in a collection. In addition to checking the "href" attribute, also checks
        that method, encoding and schema can be found from the control. Also
        validates a valid game against the schema of the control to ensure that
        they match. Finally checks that using the control results in the correct
        status code of 204.
        """

        valid = _get_person_json()

        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another game's name
        valid["username"] = "test-person-2"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # test with valid (only change model)
        valid["username"] = "test-person-1"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove field for 400
        valid.pop("model")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        """
        Checks a DELETE type control from a JSON object be it root document or an
        item in a collection. Checks the contrl's method in addition to its "href".
        Also checks that using the control results in the correct status code of 204.
        """

        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404





