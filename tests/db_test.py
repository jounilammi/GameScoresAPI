# import os
# import pytest
# import tempfile
# from sqlalchemy.engine import Engine
# from sqlalchemy import event
# from sqlalchemy.exc import IntegrityError
# from gamescoresapi.models import Person, Match, Game
# from gamescoresapi import db, create_app

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()

# @pytest.fixture
# def app():
#     db_fd, db_fname = tempfile.mkstemp()
#     config = {
#         "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
#         "TESTING": True
#     }

#     app = create_app(config)

#     with app.app_context():
#         db.create_all()

#     yield app

#     os.close(db_fd)
#     os.unlink(db_fname)



# def _get_person(word="a"):
#     '''
#     person = Person(username="NickName",
#     first_name="Testy", last_name="Tester")
#     '''
#     return(Person(username=word, first_name="Testy", last_name="Tester"))


# def _get_match(p1_id, p2_id, game_id):
#     match = Match(
#         game=game_id,
#         player1_id=p1_id,
#         player2_id=p2_id,
#         player1_score=23,
#         player2_score=30,
#         comment="well played"
#     )
#     return(match)


# def _get_game(gamename="a"):
#     game = Game(name=gamename, score_type=1)
#     return(game)


# def test_create_everything(app):
#     '''create everything and test correctness'''
#     with app.app_context():
#         # create everything
#         person1 = _get_person("aaaa")
#         person2 = _get_person("bbbb")
#         game = _get_game("tennis")
#         match = _get_match(p1_id=1, p2_id=2, game_id=1)

#         db.session.add(person1)
#         db.session.add(person2)
#         db.session.add(game)
#         db.session.add(match)

#         db.session.commit()

#         # make sure they exist
#         assert game.name == "tennis"
#         assert game.id == 1

#         assert Person.query.count() == 2
#         assert Game.query.count() == 1
#         assert Match.query.count() == 1


# def test_check_relationships(app):
#     ''' test foreign keys '''
#     with app.app_context():
#         person1 = _get_person("aaaa")
#         person2 = _get_person("bbbb")
#         game = _get_game("tennis")
#         match = _get_match(p1_id=1, p2_id=2, game_id=1)

#         db.session.add(person1)
#         db.session.add(person2)
#         db.session.add(game)
#         db.session.add(match)

#         db.session.commit()

#         assert Match.query.filter_by(id=1).first().player1_id == \
#             Person.query.filter_by(id=1).first().id
#         assert Match.query.filter_by(id=1).first().id == \
#             Game.query.filter_by(id=1).first().id
#         assert Match.query.filter_by(id=1).first().player2_id == \
#             Person.query.filter_by(id=2).first().id


# def test_unique(app):
#     '''
#     Testing uniqueness' of values that are supposed to be unique i.e. can't
#     create two identical instances
#     '''
#     with app.app_context():
#         person_1 = _get_person()
#         person_2 = _get_person()
#         # match_1 = _get_match()
#         # match_2 = _get_match()
#         game_1 = _get_game()
#         game_2 = _get_game()
#         db.session.add(person_1)
#         db.session.add(person_2)
#         # db.session.add(match_1)
#         # db.session.add(match_2)
#         db.session.add(game_1)
#         db.session.add(game_2)
#         with pytest.raises(IntegrityError):
#             db.session.commit()
#         db.session.rollback()


# def test_update(app):
#     '''Testing updating information of player with id 1'''
#     with app.app_context():
#         person = _get_person()
#         db.session.add(person)
#         db.session.commit()

#         Person.query.filter_by(id=1).update({"username": "petteri"})
#         db.session.add(person)
#         db.session.commit()
#         assert Person.query.filter_by(id=1).first().username == "petteri"


# def test_remove(app):
#     ''' test removing person from DB'''
#     with app.app_context():
#         person1 = _get_person("aaaa")
#         person2 = _get_person("bbbb")
#         game = _get_game("tennis")
#         match = _get_match(p1_id=1, p2_id=2, game_id=1)

#         db.session.add(person1)
#         db.session.add(person2)
#         db.session.add(game)
#         db.session.add(match)

#         db.session.commit()

#         Person.query.filter_by(id=1).delete()
#         db.session.commit()

#         with pytest.raises(AttributeError):
#             assert Person.query.filter_by(id=1).first().id == 1


# def test_set_null_on_delete(app):
#     ''' test that foreign key is set null when the source is deleted'''
#     with app.app_context():
#         person1 = _get_person("aaaa")
#         person2 = _get_person("bbbb")
#         game = _get_game("tennis")
#         match = _get_match(p1_id=1, p2_id=2, game_id=1)

#         db.session.add(person1)
#         db.session.add(person2)
#         db.session.add(game)
#         db.session.add(match)

#         db.session.commit()

#         Person.query.filter_by(id=1).delete()
#         db.session.commit()

#         with pytest.raises(AssertionError):
#             assert Match.query.filter_by(id=1).first().player1_id == 1
#         assert Match.query.filter_by(id=1).first().player1_id is None


# def test_foreign_key_relationship_match_to_game(app):
#     """
#     Tests that we can't assign match in a game that doesn't exist.
#     """
#     with app.app_context():
#         person1 = _get_person()
#         person2 = Person(
#             username="NickNamesss",
#             first_name="Testsssy",
#             last_name="Testssser"
#         )
#         match = Match(
#             game=1,
#             player1_id=1,
#             player2_id=2,
#             player1_score=23,
#             player2_score=33
#         )
#         db.session.add(person1)
#         db.session.add(person2)
#         db.session.add(match)
#         with pytest.raises(IntegrityError):
#             db.session.commit()
#         db.session.rollback()


# def test_foreign_key_relationship_player1_to_game(app):
#     """
#     Tests that we can't assign match in a game if player 2 is missing.
#     """
#     with app.app_context():
#         game = _get_game()
#         person1 = _get_person()
#         db.session.add(person1)
#         db.session.add(game)

#         match = Match(
#             game=1,
#             player1_id=1,
#             player2_id=2,
#             player1_score=23,
#             player2_score=33
#         )
#         db.session.add(match)
#         with pytest.raises(IntegrityError):
#             db.session.commit()
#         db.session.rollback()
