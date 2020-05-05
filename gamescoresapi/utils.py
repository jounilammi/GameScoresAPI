import json
from flask import Response, request, url_for
from .constants import *
from .models import Person, Match, Game

"""
Source and help received to game.py from
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/resource_test.py
and
https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/
"""

class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.
        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.
        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.
        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.
        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md
        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href


class GamescoresBuilder(MasonBuilder):

    def add_control_all_games(self):
        self.add_control(
            "gamsco:games-all",
            url_for("api.gamecollection"),
            method="GET",
            encoding="JSON"
        )

    def add_control_all_matches(self, game_id):
        self.add_control(
            "gamsco:matches-all",
            url_for("api.matchcollection", game_id=game_id),
            method="GET",
            encoding="JSON"
        )

    def add_control_all_persons(self):
        self.add_control(
            "gamsco:persons-all",
            url_for("api.personcollection"),
            method="GET",
            encoding="JSON"
        )

    def add_control_add_game(self):
        self.add_control(
            "gamsco:add-game",
            url_for("api.gamecollection"),
            method="POST",
            encoding="json",
            title="Add a new game",
            schema=Game.get_schema()
        )

    def add_control_add_match(self, game_id):
        self.add_control(
            "gamsco:add-match",
            url_for("api.matchcollection", game_id=game_id),
            method="POST",
            encoding="json",
            title="Add a new match for a game",
            schema=Match.get_schema()
        )

    def add_control_add_person(self):
        self.add_control(
            "gamsco:add-person",
            url_for("api.personcollection"),
            method="POST",
            encoding="json",
            title="Add a new person",
            schema=Person.get_schema()
        )

    def add_control_delete_game(self, game_id):
        self.add_control(
            "gamsco:delete-game",
            url_for("api.gameitem", game_id=game_id),
            method="DELETE",
            title="Delete this game"
        )

    def add_control_delete_match(self, game_id, match_id):
        self.add_control(
            "gamsco:delete-match",
            url_for("api.matchitem", game_id=game_id, match_id=match_id),
            method="DELETE",
            title="Delete this match"
        )

    def add_control_delete_person(self, person_id):
        self.add_control(
            "gamsco:delete-person",
            url_for("api.personitem", person_id=id),
            method="DELETE",
            title="Delete this person"
        )

    def add_control_edit_game(self, game_id):
        self.add_control(
            "edit",
            url_for("api.gameitem", game_id=game_id),
            method="PUT",
            encoding="json",
            title="Edit this game",
            schema=Game.get_schema()
        )

    def add_control_edit_match(self,game_id, match_id):
        self.add_control(
            "edit",
            url_for("api.matchitem",game_id=game_id, match_id=match_id),
            method="PUT",
            encoding="json",
            title="Edit this match",
            schema=Match.get_schema()
        )

    def add_control_edit_person(self, person_id):
        self.add_control(
            "edit",
            url_for("api.personitem", person_id=id),
            method="PUT",
            encoding="json",
            title="Edit this person",
            schema=Person.get_schema()
        )


def create_error_response(status_code, title, message=None):
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)