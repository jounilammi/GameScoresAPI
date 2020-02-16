# GameScoresAPI
## PWP SPRING 2020
## Group information
* Aleksi Sierilä Aleksi.Sierila@student.oulu.fi
* Olli Törrönen Olli.Torronen@student.oulu.fi
* Jouni Lammi Jouni.Lammi@student.oulu.fi

## How install the dependencies
The API is written in Python3. It has been tested to work with Python 3.7.2, which you can doenload from here: https://www.python.org/downloads/release/python-372/

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

## Database
The API uses a SQLite database that it runs with Flask-SQLAlchemy==2.3.2. You

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__


