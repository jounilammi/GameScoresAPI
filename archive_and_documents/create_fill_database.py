from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import Person, Game, Match, db, app, player
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.engine import Engine
# from sqlalchemy import event

db.create_all()

persons = [
    {
        "username": "Mattipee",
        "firstname": "Matti",
        "lastname": "Pulkkinen"
    },
    {
        "username": "ollitee",
        "firstname": "Olli",
        "lastname": "Torronen"
    },
    {
        "username": "alluas",
        "firstname": "aleksi",
        "lastname": "sierila"
    },
    {
        "username": "keijoal",
        "firstname": "keijo",
        "lastname": "laakso"
    },
    {
        "username": "petrikoo",
        "firstname": "petri",
        "lastname": "koski"
    },
    {
        "username": "kimmoan",
        "firstname": "kimmo",
        "lastname": "nayha"
    },
]

for person in persons:
    x = Person(
        username=person["username"],
        first_name=person["firstname"],
        last_name=person["lastname"]
    )
    db.session.add(x)
    db.session.commit()

games = [
    {
        "name": "Tennis",
        "score_type": 1  # 1 stands for more is better
    },
    {
        "name": "Golf",
        "score_type": 2  # 1 stands for less is better
    },
    {
        "name": "Running",
        "score_type": 2  # 1 stands for more is better
    },
]

for game in games:
    x = Game(
        name=game["name"],
        score_type=game["score_type"],
    )
    db.session.add(x)
    db.session.commit()

matches = [
    {
        "game": 1,
        "player1_id": 1,
        "player2_id": 2,
        "player1_score": 10,
        "player2_score": 20,

    },
    {
        "game": 2,
        "player1_id": 3,
        "player2_id": 4,
        "player1_score": 30,
        "player2_score": 40,

    },
    {
        "game": 3,
        "player1_id": 5,
        "player2_id": 6,
        "player1_score": 50,
        "player2_score": 60,

    },
]
for match in matches:
    x = Match(
        game=match["game"],
        player1_id=match["player1_id"],
        player2_id=match["player2_id"],
        player1_score=match["player1_score"],
        player2_score=match["player2_score"]
    )
    db.session.add(x)
    db.session.commit()
