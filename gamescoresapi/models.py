import click
from flask.cli import with_appcontext
from . import db

"""
Source and help received to models.py from
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/
and
https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/
"""

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
    """
    Person database table.
    username: str
    first_name: str
    last_name:  str
    birthdate: datetime (optional)
    description: str (optional)
    """
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(256), nullable=True)

    game = db.relationship("Game", secondary=player, back_populates="hobbyist")

    @staticmethod
    def get_schema():
        """Returns the schema for Person"""
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
    """
    Match database table.
    game: int: id of the game
    place: str (optional)
    time: datetime (optional)
    player1_id: int
    player2_id: int
    player1_score: float
    player2_score: float
    """
    __tablename__ = "match"
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
        """Returns the schema for Match"""
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
            "description": "ID of the game in the match",
            "type": "number"
        }
        props["player1_id"] = {
            "description": "Id of player 1 or team 1",
            "type": "number"
        }
        props["player2_id"] = {
            "description": "Id of player 1 or team 1",
            "type": "number"
        }
        props["player1_score"] = {
            "description": "Score of player 1 or team 1",
            "type": "number"
        }
        props["player2_score"] = {
            "description": "Score of player 2 or team 2",
            "type": "number"
        }
        return schema


class Game (db.Model):
    """
    Game database table.
    name: string
    score_type: int
    """
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    score_type = db.Column(db.Integer, nullable=False)

    matches = db.relationship("Match", back_populates="games")
    hobbyist = db.relationship(
        "Person", secondary=player, back_populates="game"
    )

    @staticmethod
    def get_schema():
        """Returns the schema for Game"""
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
            "type": "number"
        }
        return schema


@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Makes 'flask init-db' possible from command line. Initializes DB by
    creating the tables. Example from https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/sensorhub/models.py
    """
    db.create_all()

@click.command("testgen")
@with_appcontext
def generate_test_data():
    """
    Makes 'flask testgen' possible from command line. Fills the DB with
    sample rows. Example from https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/sensorhub/models.py
    """
    p1 = Person(
        username="user-1",
        first_name="Test",
        last_name="User"
    )
    p2 = Person(
        username="user-2",
        first_name="Test",
        last_name="User"
    )
    p3 = Person(
        username="user-3",
        first_name="Test",
        last_name="User"
    )
    g1 = Game(
        name="Tennis",
        score_type=1
    )
    g2 = Game(
        name="DiscGolf",
        score_type=2
    )

    m1 = Match(
        game=1,
        player1_id=1,
        player2_id=2,
        player1_score=45,
        player2_score=15
    )

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(g1)
    db.session.add(g2)
    db.session.add(m1)

    db.session.commit()


