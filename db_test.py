import os
import pytest
import tempfile
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from app import db, Person, Match, Game

import app

@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" +db_fname
    app.app.config["TESTING"] = True

    with app.app.app_context():
        app.db.create_all()

    yield app.db

    app.db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def _get_person():
    # person = Person(username="NickName", first_name="Testy", last_name="Tester")
    return(Person(username="NickName", first_name="Testy", last_name="Tester"))

# def _get_match():
#     match = Match(game="golf", player1_id=1, player1_score = 23, comment = "well played")
#     return(match)

def _get_game():
    game = Game(name="golf", score_type=1)
    return(game)

def test_create_everything(db_handle):
    #create everything
    person = _get_person()
    game = _get_game()
    db_handle.session.add(person)
    db_handle.session.add(game)
    db_handle.session.commit()
    #make sure they exist
    assert Person.query.count() == 1
    assert Game.query.count() == 1
    db_person = Person.query.first()
    db_game = Game.query.first()
    #check relationships
    # assert Match.query.filter(id=1).first().person1_id == Person.query.filter(id=1).first().id
    # assert Match.query.filter(id=1).first().game_id == Game.query.filter(id=1).first().id

def test_unique(db_handle):
    #Testing uniqueness' of values that are supposed to be unique i.e. can't create two identical instances
    person_1 = _get_person()
    person_2 = _get_person()
    # match_1 = _get_match()
    # match_2 = _get_match()
    game_1 = _get_game()
    game_2 = _get_game()
    db_handle.session.add(person_1)
    db_handle.session.add(person_2)
    # db_handle.session.add(match_1)
    # db_handle.session.add(match_2)
    db_handle.session.add(game_1)
    db_handle.session.add(game_2)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

def test_update(db_handle):
    #Testing updating information of player with id 1
    person = _get_person()
    db_handle.session.add(person)
    Person.query.filter_by(id=1).first().update({"username":"petteri"})
    db_handle.session.commit()

def test_remove(db_handle):
    Person.query.filter_by(id=1).delete()
    db_handle.session.commit()


def test_foreign_key_relationship_match_to_game(db_handle):
    """
    Tests that we can't assign match in a game that doesn't exist. 
    """	
    person1 = _get_person()
    person2 = Person(username="NickNamesss", first_name="Testsssy", last_name="Testssser")
    match = Match(game=1, player1_id=1, player2_id=2,player1_score = 23,player2_score = 33)
    db_handle.session.add(person1)
    db_handle.session.add(person2)
    db_handle.session.add(match)   
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

def test_foreign_key_relationship_player1_to_game(db_handle):
    """
    Tests that we can't assign match in a game if player 2 is missing. 
    """	
    game = _get_game()
    person1 = _get_person()
    match = Match(game=1, player1_id=1, player2_id=2,player1_score = 23, player2_score = 33 )
    db_handle.session.add(person1)
    db_handle.session.add(match)   
    with pytest.raises(IntegrityError):
        db_handle.session.commit()