from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Person (db.Model):
    
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    birthdate = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(256), nullable=True)

    match = db.relationship("Match", back_populates="Person")


class Match (db.Model):

    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(64), db.ForeignKey("game.id"))
    place = db.Column(db.String(64), nullable=True)
    time = db.Column(db.String(32), nullable=True)
    player1_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    player2_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    player1_score = db.Column(db.Float, nullable=False)
    player2_score = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(256), nullable=False)

    #game = db.relationship("Game", back_populates="Match")
    person1 = db.relationship("Person", foreign_keys=[Match.player1_id]) #For foreign key , back_populates="Match"
    person2 = db.relationship("Person", foreign_keys=[Match.player2_id]) #For foreign key


class Game (db.Model):
    id = db.Column(db.Integer, primary_key=True)  # integer PRIMARY KEY AUTOINCREMENT
    name = db.Column(db.String, nullable=True)
    score_type = db.Column(db.Integer, nullable=False)

    match = db.relationship("Match", back_populates="Game")




players = db.Table("players",
    db.Column("person_id", db.Integer, db.ForeignKey("person.id"), primary_key=True),
    db.Column("game_id", db.Integer, db.ForeignKey("game.id"), primary_key=True)
)


# class Player(db.Model):
#     id = db.Column(db.Integer, primary_key=True, db.ForeignKey("person.id"))  # integer PRIMARY KEY AUTOINCREMENT,
#     game = db.Column(db.String, nullable=False, db.ForeignKey("game.name"))

#     person = db.relationship("Person", back_populates="Player") #For foreign key
#     game = db.relationship("Game", back_populates="Player") #For foreign key


