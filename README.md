# GameScoresAPI
## View the api documentation in Apiary: https://gamescoresapi1.docs.apiary.io/#
## PWP SPRING 2020
## Group information
* Aleksi Sierilä Aleksi.Sierila@student.oulu.fi
* Olli Törrönen Olli.Torronen@student.oulu.fi
* Jouni Lammi Jouni.Lammi@student.oulu.fi

## How install the dependencies
The API is written in Python3. It has been tested to work with Python 3.7.2, which you can download from here: https://www.python.org/downloads/release/python-372/
Remember to select the option "Add python 3.7 to PATH".

The dependencies can be found from the requirements.txt file in the main folder. After you have installed Python3, please install the virtualenv library with
```
pip3 install virtualenv
```
After you have installed virtualenv, go to your desired folder in command prompt and type in

```
virtualenv \<insert here the virtualenv name>
```

After a successful install, type the following (Linux and MacOS):
```
source pwp/bin/activate
```

And if you are using Windows:


```
pwp\Scripts\activate.bat
```

Now your command prompt should have the virtualenv name next to the default prompt.

Clone this git repository and enter its main folder in your command prompt. Install the dependencies by typing

```
pip3 install -r requirements.txt
```

After a successful install you now have a working virtualenv to run this API. You can deactivate the virtualenv by just typing
```deactivate``` into your prompt.

## Running the api
Navigate to .../GameScoresAPI/ and give the following commands  
Windows:  
```
set FLASK_APP=gamescoresapi
set FLASK_ENV=development
flask init-db # if you do not have a database instance and need to create one
flask testgen # if you want to fill the database with example data
flask run
```
Linux/Mac:  
```
export FLASK_APP=gamescoresapi
export FLASK_ENV=development
flask init-db # if you do not have a database instance and need to create one
flask testgen # if you want to fill the database with example data
flask run
```
## Database
The API uses a SQLite database that it runs with Flask-SQLAlchemy==2.3.2. You
### How to populate the database
Open a Python3 prompt. Enter the following commands:

```python
from app import Person, Game, Match, db
db.create_all()

person1 = Person(username="Mattipee", first_name="Matti", last_name="Pulkkinen")
person2 = Person(username="Janiee", first_name="Jani", last_name="Eerola")

db.session.add(person1)
db.session.add(person2)
db.session.commit()

game1 = Game(id=1, name="Cottage darts", score_type=1)
db.session.add(laji)
db.session.commit()

match1 = Match(
        game=1,
        player1_id=1,
        player2_id=2,
        player1_score=50,
        player2_score=32
    )
db.session.add(match1)
db.session.commit()
```

You have now a populated database with one match.

## Testing

GameScoresAPI is tested with Python3's ```pytest``` library. When you have the ```virtualenv``` activated, navigate into the main folder of the GameScoresAPI and give the command ```pytest```. The tests run automatically.

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__


