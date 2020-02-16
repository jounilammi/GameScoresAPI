from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.engine import Engine
# from sqlalchemy import event


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Person (db.Model):
    # __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    birthdate = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(256), nullable=True)

    # match1 = db.relationship("Match", backref="person")
    # match2 = db.relationship("Match", back_populates="person2")


class Match (db.Model):
    # __tablename__ = "match"
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(64), db.ForeignKey("game.id"))
    place = db.Column(db.String(64), nullable=True)
    time = db.Column(db.String(32), nullable=True)
    player1_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    player2_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    player1_score = db.Column(db.Float, nullable=False)
    player2_score = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(256), nullable=True)

    games = db.relationship("Game", back_populates="matches")
    person = db.relationship(
        "Person",
        foreign_keys="Match.player1_id",
        # back_populates="Person.match1"
        # back_populates="Person.match1"

    )

    person2 = db.relationship(
        "Person",
        foreign_keys="Match.player2_id",
        # back_populates="match2"
    )
# pee = Person(username="jN",first_name="Janne",last_name="Neuvo")


class Game (db.Model):
    # __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)  # integer PRIMARY KEY AUTOINCREMENT
    name = db.Column(db.String, nullable=True, unique=True)
    score_type = db.Column(db.Integer, nullable=False)

    matches = db.relationship("Match", back_populates="games")


player = db.Table("player",
    db.Column("person_id", db.Integer, db.ForeignKey("person.id"), primary_key=True),
    db.Column("game_id", db.Integer, db.ForeignKey("game.id"), primary_key=True)
)


# class Player(db.Model):
#     id = db.Column(db.Integer, primary_key=True, db.ForeignKey("person.id"))  # integer PRIMARY KEY AUTOINCREMENT,
#     game = db.Column(db.String, nullable=False, db.ForeignKey("game.name"))

#     person = db.relationship("Person", back_populates="Player") #For foreign key
#     game = db.relationship("Game", back_populates="Player") #For foreign key


#from app import Person, Match, Game
#from app import db
#db.create_all()
#joo = Person(id=1, username="joa", first_name="jjj", last_name="fjfj")
#db.session.add(joo)
#db.session.commit()
#laji = Game(id=1, name="golf", score_type=1)
#db.session.add(laji)
#db.session.commit()
#ottelu = Match(id=1, game="golf", player1_id=1, player1_score = 23, comment = "fjdsf")
#db.session.add(ottelu)
#db.session.commit()
#Match.query.all()
#Person.query.first().match1
#jne
#
#
#>>> Match.query.first().player1_score
#23.0
#>>> Match.query.first().games                ei printtaa mitään?
#>>>
#>>> Match.query.first().person1
#<Person 1>


#>>> Person.query.first().match1
#[<Match 1>]

#>>> Match.query.first().games
#>>>
#>>> Match.query.first().person1
#<Person 1>

#>>> Game.query.first().matches       miksi tyhjä lista?
#[]