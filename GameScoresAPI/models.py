import click
from flask.cli import with_appcontext
from GameScoresAPI import db


player = db.Table(
    "player",
    db.Column(
        "person_id", db.Integer, db.ForeignKey("person.id"), primary_key=True
    ),
    db.Column(
        "game_id", db.Integer, db.ForeignKey("game.id"), primary_key=True
    )
)


class Person (db.Model):
    # __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(256), nullable=True)

    game = db.relationship("Game", secondary=player, back_populates="hobbyist")

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["username", "first_name", "last_name"]
        }
        props = schema["properties"] = {}
        props["username"] = {
            "description": "Person's username",
            "type": "string"
        }
        props["first_name"] = {
            "description": "Person's first name",
            "type": "string"
        }
        props["last_name"] = {
            "description": "Person's last name",
            "type": "string"
        }
        return schema


class Match (db.Model):
    # __tablename__ = "match"
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(
        db.Integer,
        db.ForeignKey("game.id", ondelete="SET NULL"),
        nullable=True
    )
    place = db.Column(db.String(64), nullable=True)
    time = db.Column(db.DateTime, nullable=True)
    player1_id = db.Column(
        db.Integer,
        db.ForeignKey("person.id", ondelete="SET NULL"),
        nullable=True
    )
    player2_id = db.Column(
        db.Integer,
        db.ForeignKey("person.id", ondelete="SET NULL"),
        nullable=True
    )
    player1_score = db.Column(db.Float, nullable=False)
    player2_score = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(256), nullable=True)

    games = db.relationship("Game", back_populates="matches")
    person = db.relationship(
        "Person",
        foreign_keys="Match.player1_id",
    )

    person2 = db.relationship(
        "Person",
        foreign_keys="Match.player2_id",
    )

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": [
                "game",
                "player1_id",
                "player2_id",
                "player1_score",
                "player2_score"
            ]
        }
        props = schema["properties"] = {}
        props["game"] = {
            "description": "Name of the game in the match",
            "type": "string"
        }
        props["player1_id"] = {
            "description": "Id of player 1 or team 1",
            "type": "string"
        }
        props["player2_id"] = {
            "description": "Id of player 1 or team 1",
            "type": "string"
        }
        props["player1_score"] = {
            "description": "Score of player 1 or team 1",
            "type": "string"
        }
        props["player2_score"] = {
            "description": "Score of player 2 or team 2",
            "type": "string"
        }
        return schema


class Game (db.Model):
    # __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    score_type = db.Column(db.Integer, nullable=False)

    matches = db.relationship("Match", back_populates="games")
    hobbyist = db.relationship(
        "Person", secondary=player, back_populates="game"
    )

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["name", "score_type"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Name of the game",
            "type": "string"
        }
        props["score_type"] = {
            "description": "Score type of the game",
            "type": "string"
        }
        return schema

