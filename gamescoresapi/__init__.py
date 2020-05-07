import os
import json
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from .constants import (
    MASON,
    LINK_RELATIONS_URL,
    ERROR_PROFILE,
    GAME_PROFILE,
    MATCH_PROFILE,
    PERSON_PROFILE,
    MEASUREMENT_PAGE_SIZE
)

"""
Source and help received to _init_.py from
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/resource_test.py
and
https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/
"""

db = SQLAlchemy()

# Based on http://flask.pocoo.org/docs/1.0/tutorial/factory/#the-application-factory
# Modified to use Flask SQLAlchemy
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join("development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from . import models
    from . import api
    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.generate_test_data)
    app.register_blueprint(api.api_bp)

    @app.route(LINK_RELATIONS_URL)
    def send_link_relations():
        return "link relations"

    @app.route("/profiles/<profile>/")
    def send_profile(profile):
        return "you requests {} profile".format(profile)

    @app.route("/admin/")
    def admin_site():
        return app.send_static_file("html/admin.html")

    @app.route("/api/")
    def index():
        body = {
            "@namespaces": {
                "gamsco": {
                    "name": "/gamescores/link-relations/#"
                }
            },
            "@controls": {
                "gamsco:persons-all": {
                    "href": "/api/persons/"
                },
                "gamsco:matches-all": {
                    "href": "/api/games/{game_id}/matches/"
                },
                "gamsco:games-all": {
                    "href": "/api/games/"
                }
            }
        }
        return Response(
            status=200,
            response=json.dumps(body),
            mimetype=MASON
        )

    return app
