import json
import os
import pytest
import tempfile
import time
from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

from ..gamescoresAPI import db, app
from ..gamescoresAPI.api import api
from ..gamescoresapi.resources.game import GameCollection, GameItem
from ..gamescoresapi.resources.match import MatchCollection, MatchItem
from ..gamescoresapi.resources.person import PersonCollection, PersonItem
from ..gamescoresapi.models import Game, Match, Person


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


def _get_game(gamename="a"):
    game = Game(name=gamename, score_type=1)
    return(game)

def _populate_db():
    """
    Pre-populate database with 2 matches, 2 players and 2 matches
    """

    person1 = _get_person("aaaa")
    person2 = _get_person("bbbb")
    game = _get_game("tennis")
    game2 = _get_game("golf")
    match = _get_match(p1_id=1, p2_id=2, game_id=1)
    match = _get_match(p1_id=1, p2_id=2, game_id=2)

    db_handle.session.add(person1)
    db_handle.session.add(person2)
    db_handle.session.add(game)
    db_handle.session.add(game2)
    db_handle.session.add(match)
    db_handle.session.add(match2)

    db_handle.session.commit()

def _check_namespace(client, response):
    """
    Checks that the "kyykka" namespace is found from the response body, and
    that its "name" attribute is a URL that can be accessed.
    """

    ns_href = response["@namespaces"]["kyykka"]["name"]
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



def _check_control_post_method_player(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
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
    body = _get_player_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201