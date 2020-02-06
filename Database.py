from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Persons (
    id integer PRIMARY KEY AUTOINCREMENT,
    username string,
    first_name string,
    last_name string,
    birthdate string,
    description string
);

class Matches (
    id integer PRIMARY KEY AUTOINCREMENT,
    game string,
    place string,
    time string,
    player1_id integer,
    player2_id integer,
    player1_score float,
    player2_score float,
    comment string
);

class Games (
    id integer PRIMARY KEY AUTOINCREMENT,
    name string,
    score_type integer
);

CREATE TABLE Player (
    id integer,
    game string
);
