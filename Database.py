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
