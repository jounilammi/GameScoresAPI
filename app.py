from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///GameScoresApiDB.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


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


class Game (db.Model):
    # __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    score_type = db.Column(db.Integer, nullable=False)

    matches = db.relationship("Match", back_populates="games")
    hobbyist = db.relationship(
        "Person", secondary=player, back_populates="game"
    )
